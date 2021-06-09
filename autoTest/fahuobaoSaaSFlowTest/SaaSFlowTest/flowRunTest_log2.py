# import logging,logging.handlers
import os
import datetime
import time
from loggingTest import myLog

caselist=(os.chdir('../FlowTestCase'))
print("当前工作目录:",os.getcwd())
testlist=[]
for testflow in os.listdir(caselist):
	if testflow=='__init__.py':
		pass
	else:
		testlist.append(testflow)
		os.system(testflow)
print(testlist)

if __name__=="__main__":
    myLog()