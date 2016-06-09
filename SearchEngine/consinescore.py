#coding=utf-8
from __future__ import division
import jieba
import os
import os.path
import re
import json
import io
import sys, locale
import math
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def make_doc_list():
	doc_list = []
	for term in indexTable:
		posting_list = indexTable[term];
		for posting in posting_list:
			doc = posting['doc']
			if doc_list.count(doc)==0:
				doc_list.append(doc)
	return doc_list

def ComputeDocLength():
	Length = {}
	for doc in doc_list:
		Length[doc] = 0
	for term in indexTable:
		posting_list = indexTable[term];
		for posting in posting_list:
			doc = posting['doc']
			tf = posting['tf']
			df = len(posting_list)
			TotalDoc = len(doc_list)
			weight = (1+math.log10(tf))*math.log10(TotalDoc/df)
			Length[doc] += weight**2;
	for doc in doc_list:
		Length[doc] = math.sqrt(Length[doc])
	return Length

			
def ConsineScore(query):
	query.decode(sys.stdin.encoding or locale.getpreferredencoding(True))
	Score = {}
	for doc in doc_list:
		Score[doc] = 0
	TotalDoc = len(doc_list)
	query_term_list = jieba.lcut_for_search(query)
	for term in query_term_list:
		try:
			posting_list = indexTable[term];
		except:
			continue
		for posting in posting_list:
			doc = posting['doc']
			tf = posting['tf']
			df = len(posting_list)
			weight = (1+math.log10(tf))*math.log10(TotalDoc/df)
			Score[doc] += weight;
	for doc in doc_list:
		Score[doc] = Score[doc]/doc_length[doc];
	return sorted(Score.iteritems(), key=lambda d:d[1], reverse = True)[:10]	#返回排名前十的页面 list[(doc_id,score)...]

with io.open('./my_index.json', 'r', encoding='utf-8') as f:
	data=f.read()
indexTable=json.loads(data)
doc_list = make_doc_list()
doc_length = ComputeDocLength()

	result = ConsineScore(u'研究')
	for doc in result:
		print doc