import sys
import os
import os.path
import re
import string
import socket
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import time
from whoosh.index import create_in
from whoosh.fields import *

f=open('doc_index.txt','r')
doc_index=eval(f.read())
f.close()
len=len(doc_index)
print(len)


schema = Schema(id=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))
ix = create_in('index', schema)
writer = ix.writer()

i=0
for did,doci in doc_index.items():
	i+=1
	print(str(i)+'/'+str(len))
	
	writer.add_document(id=did,title=doci['title'],content=doci['body'])

writer.commit()
