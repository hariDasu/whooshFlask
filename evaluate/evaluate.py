#!/usr/bin/env python3
#--------------------------------------
# vi:  sw=4 ts=4 expandtb ai
#--------------------------------------
import sys
import os
import os.path
import re
import string
import socket
from xml.etree import ElementTree
import time
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh import scoring
import json



#topic = '152'
#query = 'Accusations of Cheating by Contractors on U.S. Defense Projects'
	
jfile = open('judgement/qrels.151-200.disk1.disk2.part1','r')
judg = jfile.read()
jfile.close()
jfile = open('judgement/qrels.151-200.disk1.disk2.part2','r')
judg += jfile.read()
jfile.close()
jfile = open('judgement/qrels.151-200.disk1.disk2.part3','r')
judg += jfile.read()
jfile.close()
jfile = open('judgement/qrels.151-200.disk1.disk2.part4','r')
judg += jfile.read()
jfile.close()
jfile = open('judgement/qrels.151-200.disk1.disk2.part5','r')
judg += jfile.read()
jfile.close()

topicfile = open('topic_dict.txt','r')
topic_dict = eval(topicfile.read())
topicfile.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#input: topic number, top-n results
#output: pre,rec,f at top n
def evaluate(topicnum,n):
	
	query = topic_dict[topicnum]

	reg = re.compile(str(topicnum)+'\s0\sWSJ8.+\s\d')
	rel = reg.findall(judg)


	ix = open_dir('index')

	searcher = ix.searcher()

	query_terms = query.split(' ')
	bool_query = ''
	for term in query_terms:
		bool_query += term + ' OR '
	parser = QueryParser("content", ix.schema)
	real_query = parser.parse(bool_query)
	results = searcher.search(real_query, limit = n)

	res = []
	for i in results:
		res.append(i['id'])


	tp=0
	for resi in res:
		for reli in rel:
			if resi in reli:
				tp+=1
				
	if len(res)==0 or len(rel)==0:
		return [0,0,0]
	
	pre = tp/len(res)
	rec = tp/len(rel)
	f = 2*pre*rec/(pre+rec)
	
	return [pre,rec,f]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def doEvaluate(topic=151,n=50) :
    avgpre=0
    avgrec=0
    avgf=0

    res = evaluate(topic,n)
    avgpre+= res[0]
    avgrec+= res[1]
    avgf+= res[2]


    values = json.dumps([avgpre,avgrec,avgf])
    return (values)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__" :
    doEvaluate(151,50)
