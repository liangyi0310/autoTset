# -*- coding: utf8 -*-

import os

import time

from HTMLTestRunner import HTMLTestRunner

caselist=(os.chdir('./FlowTestCase'))
print("当前工作目录:",os.getcwd())
testlist=[]
for testflow in os.listdir(caselist):
	if testflow=='__init__.py':
		pass
	else:
		testlist.append(testflow)
		os.system(testflow)
print(testlist)
