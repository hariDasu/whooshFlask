import sys
import os
import os.path
import re
import string
import socket
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import time

dict={}
rootdirs=[]
rootdirs.append('/volumes/i/trec/1/wsj/1987/')
rootdirs.append('/volumes/i/trec/1/wsj/1988/')
rootdirs.append('/volumes/i/trec/1/wsj/1989/')

s=0
for rootdir in rootdirs:
	for parent,dirnames,filenames in os.walk(rootdir):
		for filename in filenames:
			if '.Z' not in filename:		

				f=open(rootdir+filename,'r')
				doc=f.read()
				f.close()
				#doc=doc.replace('\n',' ')
				#print(rootdir+filename)
				
				re_docno=re.compile('<DOCNO>.*</DOCNO>')
				docno=re_docno.findall(doc)

				for i in range(0,len(docno)-1):
					docno[i]=docno[i].split('<DOCNO>')[1]
					docno[i]=docno[i].split('</DOCNO>')[0]
					docno[i]=docno[i].strip(' ')
				
				dochl=doc.split('</HL>')
				for i in range(0,len(dochl)-1):
					if '<HL>' in dochl[i]:
						dochl[i]=dochl[i].split('<HL>')[1]
						p=re.compile(r'\W')
						dochl[i]=p.sub(' ',dochl[i])
						dochl[i]=re.sub(" +",' ',dochl[i])
						dochl[i]=dochl[i].strip(' ')
				#print(len(dochl))
				
				tp1=doc.split('</TEXT>')
				for i in range(0,len(tp1)-1):
					if '<TEXT>' in tp1[i]:
						tp1[i]=tp1[i].split('<TEXT>')[1]
						p=re.compile(r'\W')
						tp1[i]=p.sub(' ',tp1[i])
						tp1[i]=re.sub(" +",' ',tp1[i])
						tp1[i]=tp1[i].strip(' ')
				
				for i in range(0,len(docno)-1):
					doci={}
					doci['title']=dochl[i]
					doci['body']=tp1[i]
					dict[docno[i]]=doci
				
				

f=open('doc_index.txt','w')
f.write(str(dict))
f.close()




		

