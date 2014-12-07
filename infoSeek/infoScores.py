#!/usr/bin/env  python3
#------------------------------------
# vi: sw=4 ts=4 expandtab
#------------------------------------
import sys
import os
import os.path
import re
import string
import socket
import pudb
from pprint import PrettyPrinter
import time
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh import scoring
import math
import json
import collections
from evaluate.evaluate import doEvaluate
from spellCheck.correct import doyoumean
from spellCheck.correct import correct2

pp=PrettyPrinter(indent=4)
retModel= {
  "BM25F"  :  scoring.BM25F,
  "TFIDF"  :  scoring.TF_IDF,
"termFreq" :  scoring.Frequency         
}
defQueryString='coping overcrowded prisons '

class InfoSeeker(object) :

    #--------------------------------------------------------
    def   __init__(self)  :
        pass

    #--------------------------------------------------------
    def eMim(self, na,nb,nab,N):
        score=0;
        if(na>0 and nb>0 and nab>0):
            try:
                score = (nab)*math.log((N)*((nab)/(na*nb)))
            except Exception:
                print(na,nb,nab,N);
        return score
    #--------------------------------------------------------
    def chiSquare(self, na,nb,nab,N):
        score=0;
        if(na>0 and nb>0):
            score = (math.pow((nab-(1/N)*na*nb), 2))/(na*nb)
        return score

    #--------------------------------------------------------
    def dices(self, na,nb,nab,N):
        score=0;
        if(na>0 and nb>0):
            score = (nab)/(na+nb)
        return score

    #--------------------------------------------------------
    def mim(self, na,nb,nab,N):
        score=0;
        if(na>0 and nb>0):
            score=(nab)/(na*nb)
        return score
    #--------------------------------------------------------
    def findCandidateWords(self, topTenDocs):
        retWords=set();
        for oneDoc in topTenDocs:
            wordsInDoc=[ w.lower()  for w in oneDoc['content'].split() ]
            for word in wordsInDoc:
                with open("stopwords.txt") as f:
                    stopwords=f.read()
                    stopworded=' '.join(stopwords.split())
                    if word not in stopworded:
                        retWords.add(word);
        return list(retWords);
    #--------------------------------------------------------
    def wordInDocs(self, allDocs,lookupWord):
        docCount=0;
        for doc in allDocs:
            if lookupWord in doc['content']:
                docCount+=1;
        return(docCount)
    #--------------------------------------------------------
    def bothWordsInDoc(self, allDocs,lookupWordA,lookupWordB):
        docCount=0;
        for document in allDocs:
            if lookupWordA in document['content'] and lookupWordB in document['content']:
                docCount+=1;
        return(docCount)
    #--------------------------------------------------------
    def buildScores(self, allDocs,queryTerms,candidateWords):
        scores={};
        for a in queryTerms:
            for b in candidateWords:
                na=self.wordInDocs(allDocs,a);
                nb=self.wordInDocs(allDocs,b);
                nab=self.bothWordsInDoc(allDocs,a,b);
                eMimScore=self.eMim(na,nb,nab,len(allDocs));
                diceScore=self.dices(na,nb,nab,len(allDocs));
                mimScore=self.mim(na,nb,nab,len(allDocs));
                chiSquareScore=self.chiSquare(na,nb,nab,len(allDocs));
                if not a in scores :
                    scores[a]={}
                if not 'eMim' in scores[a]:
                    scores[a]['eMim']={}
                    scores[a]["dices"]={}
                    scores[a]["mim"]={}
                    scores[a]["chiSquare"]={}
                scores[a]['eMim'][b]=eMimScore;
                scores[a]['dices'][b]=diceScore;
                scores[a]['mim'][b]=mimScore;
                scores[a]['chiSquare'][b]=chiSquareScore;
        return scores;
    #--------------------------------------------------------
    def bestWords(self, scores,queryTerm,metric):
        wordScores=scores[queryTerm][metric]
        sortedTerms=sorted(wordScores, key=wordScores.get, reverse=True)
        i=0

        res=""
        for oneTerm in sortedTerms :
            if oneTerm == queryTerm :
                continue
            res+=(queryTerm+ ":"+oneTerm  + "<br>")
            i+=1
            if i == 10 :
                break
        res+="<HR>"
        return res
    #----------------------------
    def bestWords2(self, scores ):
        res=""
        for queryTerm in scores.keys() :
            res+="<H3>" + queryTerm + "</H3>\n"
            res+="<table><tr><th>"
            zipScores=[]
            for metric in scores[queryTerm].keys() :
                res+="<th>" + metric
                wordScores=scores[queryTerm][metric]
                sortedTerms=sorted(wordScores, key=wordScores.get, reverse=True)
                zipScores.append(sortedTerms[:20])
            res+="</tr>\n"
            # print (zipScores)

            for i in range(10) :
                res+="<tr><td>" + str(i+1)
                for j in range(4) :
                    datum=zipScores[j][i]
                    res+="<td>" + datum
                res+="</tr>\n"
            res+="</table>\n"
            #print(res)
        return res
    #----------------------------
    def initSeeker(self, retrMethod="BM25F")  :
        ix = open_dir('index')
        retrModel=retModel[retrMethod]
        if retrMethod !="BM25F":
            self.searcher=ix.searcher(weighting=retrModel())
        else:
            self.searcher = ix.searcher(weighting=retrModel(B=0.75, content_B=1.0, K1=1.5))
        self.parser = QueryParser("content", ix.schema)

    #--------------------------
    def initQuery(self, userQueryString=defQueryString, expModel="noExp") :
        retDict=collections.OrderedDict();
        uQuery=" OR ".join( userQueryString.split() )
        myquery = self.parser.parse(uQuery)
        #print(myquery)
        results = self.searcher.search(myquery)
        numResults = len(results)
        print(len(results))
        qTerms=userQueryString.replace(" OR ", " ").replace(" AND ", " ").split()
        topTenDocs =results[:10]
        wc=self.findCandidateWords(topTenDocs);
        #print(topTenDocs)
        scores=self.buildScores(results,qTerms,wc);
        suggest=' '.join(qTerms)
        print(suggest)
        if ' ' in suggest:
            suggestions = doyoumean(suggest);
            print (suggestions)
        else:
            suggestions = correct2(suggest);
        retDict["suggestions"]=suggestions;
        retDict["numResults"]=numResults;
        #pp.pprint(scores);
        #return self.bestWords2(scores)
        expansionWords=""
        #----------------------- 
        if  expModel == "noExp" :
            expansionWords+="No Expansion ...."
            for oneDoc in topTenDocs:
                title=oneDoc["title"];
                content=oneDoc.highlights("content");
                if not title in retDict:
                    retDict[title]=content;
        else :
            for term in qTerms:
                expansionWords+=self.bestWords(scores, term, expModel)
            for oneDoc in topTenDocs:
                retDict[oneDoc["title"]]=(oneDoc.highlights("content"))
                retDict["expTerms"]=expansionWords
        #----------------------- 
        stringed=json.dumps(retDict);
        return stringed
        
        """
        """

if __name__ == "__main__" :
    is1=InfoSeeker()
    is1.initSeeker()
    pp.pprint(is1.initQuery() )


