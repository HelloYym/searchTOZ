# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import os.path
import jieba
import re
import json
import io
import sys, locale

with io.open('./my_index.json', 'r', encoding='utf-8') as f:
	data=f.read()
indexTable=json.loads(data)
k=raw_input("输入索引： ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
# k=k.decode('utf-8').encode('utf-8')
print indexTable[k]