# -*- coding: utf-8 -*-
import os
import os.path
import jieba
import re
import json
import io

dirlist=['./mypage.zju.edu.cn',
		'./person.zju.edu.cn',
]
#Posting store in indexNode.postingLists
class Posting():
	def __init__(self, doc, tf):
		self.doc = doc            #doc will be the filename of doc
		self.tf = tf

indexTable=dict()  # hashtable to store all index
handledFilename=[]
for rootdir in dirlist:
	for parent,dirnames,filenames in os.walk(rootdir):
		for relative_filename in filenames:
			filename=rootdir+"/"+relative_filename
			# print filename
			if filename in handledFilename:
				print "duplicate!!"
			handledFilename.append(filename)
			with open(filename,"r") as f:
				text=f.read().decode('utf-8').encode('utf-8')
			text=re.sub("\{.*?\}","",text)
			text=" ".join(text.split())
			# print text
			seg_list=jieba.cut_for_search(text)
			seg_list=list(seg_list)
			handled_list=[]
			# print type(seg_list)
			for term in [x for x in seg_list if x not in handled_list]:  #这列临时的list做好后，不会因后面的改变而改变
				if term in handled_list:
					continue
				if term not in indexTable:     # A new term without index
					# print "new index"
					new_post=dict()
					new_post['doc']=filename
					new_post['tf']=seg_list.count(term)
					# new_post=Posting(filename,seg_list.count(term))  #create a posting
					new_postingLists=[]                        #create a postinglists
					new_postingLists.append(new_post)
					indexTable[term]=new_postingLists
				else:
					# print "upate index"
					new_post=dict()
					new_post['doc']=filename
					new_post['tf']=seg_list.count(term)
					# new_post=Posting(filename,seg_list.count(term))  #extend postinglists
					indexTable[term].append(new_post)
				handled_list.append(term)
# print indexTable
print "index completed!"
for k in indexTable:
	print k

# with open("./my_index.json","w") as f:
# 	json.dump(indexTable,f,ensure_ascii=False)

with io.open('./my_index.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(indexTable, ensure_ascii=False)))
