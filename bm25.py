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
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh import scoring
import math

#input: query string
#output: top-n relevant document with their bm25 score

def bm25_retrieve (query, num_res):
	ix = open_dir('index')
	searcher = ix.searcher()
	query_terms = query.split(' ')
	bool_query = ''
	for term in query_terms:
		bool_query += term + ' OR '
	parser = QueryParser("content", ix.schema)
	real_query = parser.parse(bool_query)
	results = searcher.search(real_query, limit = num_res)
	
	new_results = {}
	res_len = len(results)
	
	#assume that top 10 results is relevant
	
	ri = {}
	ni = {}
	R = 10
	N = res_len

	for term in query_terms:
		ri[term] = 0
		ni[term] = 0
	
	#for each term in the query, calculate its ri and ni
	for term in query_terms:
		for res in searcher.search(real_query):
			if term in res['content']:
				ri[term] += 1
		parser = QueryParser("content", ix.schema)
		term_query = parser.parse(term)
		ni[term] = len(searcher.search(term_query, limit = 500))
	
	#for each document, calculate its bm25 score
	if num_res > 10:
		for res in results:
			new_results[res['id']] = 0
		for res in results:
			for term in query_terms:
				reg = re.compile(term)
				#fi is the i's term's frequency in the document
				fi = len(reg.findall(res['content']))
				k1 = 1.5
				b = 0.75
				avdl = 200
				K = k1 * (1 - b + b * len(res['content']) / 200)
				new_results[res['id']] += math.log((ri[term]+0.5)*(N-ni[term]-R+ri[term]+0.5)/(R-ri[term]+0.5)/(ni[term]-ri[term]+0.5)) * (k1 + 1) * fi / (K + fi)
				
	return new_results

res = bm25_retrieve('tropical fish',20)

print(res)