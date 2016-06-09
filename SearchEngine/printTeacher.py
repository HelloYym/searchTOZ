# -*- coding: utf-8 -*-
import os
import os.path
import jieba
import re
import json
import io

def teacherInfo(filename):
	with open(u'./mypage.zju.edu.cn/weblog_IGB.txt',"r") as f:
		text=f.read()
	d=eval(text)
	#print info
	for k,v in d.iteritems():
		try:
			if k=="intro":
				print k+": "+v[0]
			else:
				print k+": "+v
		except:
			print k+": None"

	# print "-------教师信息--------"
	# # try:
	# print "姓名:"+d['name'][0]
	# # except:
	# print "姓名： "+"暂缺"

	# try:
	# 	print "部门： "+d['department'][0]
	# except:
	# 	print "部门： "+"暂缺"

	# try:
	# 	print "职称： "+d['title'][0]
	# except:
	# 	print "职称： "+"暂缺"

	# try:
	# 	print "个人主页： "+d['homepage']
	# except:
	# 	print "个人主页："+"暂缺"

	# try:
	# 	print "博客： "+d['blog'][0]
	# except:
	# 	print "博客： "+"暂缺"

if __name__ == "__main__":
	teacherInfo(u'./teachers/760.txt')