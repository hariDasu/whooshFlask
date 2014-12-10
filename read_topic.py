import sys
import os
import os.path
import re
import string
import socket
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import time

f=open('topic/topics.151-200','r')
topics=f.read()
f.close()
topics=topics.replace('\n',' ')
dict={}

reg=re.compile('<num>(.*?)<desc>')
res=reg.findall(topics)
i = 151
for resi in res:
	resi = resi.split('Topic:')[1]
	resi = resi.strip(' ')
	dict[i]=resi
	i += 1
print(dict)
f=open('topic_dict.txt','w')
f.write(str(dict))
f.close()