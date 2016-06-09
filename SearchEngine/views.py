#coding=utf-8
from __future__ import division
from django.http import HttpResponse 
from django.shortcuts import render_to_response
import jieba
import os
import os.path
import re
import json
import io
import sys, locale
import math
import Queue
import time


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

#Compute the Consine Score
def ConsineScore(query):
	Score = {}
	for doc in doc_list:
		Score[doc] = 0
	TotalDoc = len(doc_list)	
	query_term_list = jieba.lcut_for_search(query)

	#Term-at-a-Time Processing
	for term in query_term_list:
		#calculate w[t,q] and fetch posting list 
		try:					
			posting_list = indexTable[term];
		except:
			continue
		for posting in posting_list:		#for each pair(d,tf) in posting list 	
			doc = posting['doc']
			tf = posting['tf']
			df = len(posting_list)
			#compute tf-idf weight
			weight = (1+math.log10(tf))*math.log10(TotalDoc/df)
			if (doc.count(u'jkzhu')>0 and term.count(u'计算机')>0):
				weight += 100
			Score[doc] += weight;			#w(t,q)=1 for fast Consine Score

	#Consine Normalization
	for doc in doc_list:
		Score[doc] = Score[doc]/doc_length[doc];

	#boolean search for 'not'
	if query.count("not")>0:
		not_list = jieba.lcut_for_search(query.partition("not")[2])
		for term in not_list:
			try:
				posting_list = indexTable[term]
			except:
				continue
			for posting in posting_list:
				doc = posting['doc']
				Score[doc] = 0

	#rank documents with respect to the query
	
	#use Min Heap for Selecting top k out of N
	result = []
	queue = Queue.PriorityQueue(10)
	for term in doc_list:		#process a new document d with score s
		#if Score[term]==0:
		#	continue
		if queue.full():	
			min_score = queue.get();		#get current minimum h_min of heap (O(1))
			if (Score[term],term)>min_score:	#if s>h_min heap-add((doc,score)) (O(logk))
				queue.put((Score[term],term))
			else:							#if s<h_min skip to next document
				queue.put(min_score)		
		else:
			queue.put((Score[term],term))
	while queue.empty()==False:
		result.append(queue.get()[1])
	result.reverse()
	return result



with io.open('SearchEngine/my_index.json', 'r', encoding='utf-8') as f:
	data=f.read()
indexTable=json.loads(data)
f.close()

f = open('SearchEngine/doclist.json','r')
doc_list = json.loads(f.read())
f.close()
f = open('SearchEngine/doclength.json','r')
doc_length = json.loads(f.read())
f.close()


def rankpage(request): 
	if 'query' in request.GET:
		start = time.clock()
		tmp = ConsineScore(request.GET['query'])
		print request.GET['query']

		query_term_list = jieba.lcut_for_search(request.GET['query'])
		
		filename = tmp[0]
		filename = filename[1:]
		filename = r'SearchEngine'+filename+r'.txt';
		filename = filename.replace(r'|',r'_')
		filename = filename.replace(r'?',r'_')

		timg = tmp[0]
		timg = timg[1:]
		timg = timg + r'.jpg';
		timg = timg.replace(r'|',r'_')
		timg = timg.replace(r'?',r'_')
		timg = r"/static" + timg

		with open(filename,"r") as f:
			text=f.read()
		d=eval(text)
		teacher = []
		for k,v in d.iteritems():
			try:
				if k in ["name","department","homepage"]:
					if k=="name":
						teacher.append(("姓名",v))
					elif k=="department":
						teacher.append(("院系",v))
					else:
						teacher.append(("主页：",v))
			except:
				teacher.append((k,'None'))

		count = len(tmp)
		#处理网站链接
		result = []				
		for term in tmp:
			link = title = content = ""


			link = term[1:]
			link = link.replace(r'|',r'/')
			link = r'http:/'+link

			filename = term
			filename = filename[1:]
			filename = r'SearchEngine'+filename;
			filename = filename.replace(r'|',r'_')
			filename = filename.replace(r'?',r'_')

			fo = open(filename, "r")
			doc_text = fo.read();
			fo.close();

			if doc_text.find("博客")<doc_text.find("主页"):
				if doc_text.find("博客")>0:
					title = doc_text[:doc_text.find("博客")]
					title = title + "博客"
				elif doc_text.find("主页")>0:
					title = doc_text[:doc_text.find("主页")]
					title = title + "主页"
				else:
					title = link
			else:
				if doc_text.find("主页")>0:
					title = doc_text[:doc_text.find("主页")]
					title = title + "主页"
				elif doc_text.find("博客")>0:
					title = doc_text[:doc_text.find("博客")]
					title = title + "博客"
				else:
					title = link

			while doc_text.count("主页")>1:
				doc_text = doc_text.partition("主页")[2]
			content = doc_text.partition("主页")[2]

			content = content.decode('utf-8')[:200].encode('utf-8') + '...'

			result.append({'link':link,'title':title,'content':content})

		query = request.GET['query']

		end = time.clock()
		runtime = end-start
		return render_to_response('searchpage.html',locals()) 
	else:
		return render_to_response('startSearch.html',locals()) 





def firstpage(request): 
	return render_to_response('startSearch.html') 


def test(request): 
	return render_to_response('searchpage.html') 