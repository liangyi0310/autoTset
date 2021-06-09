import os
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from Common.readConfig import *


os.chdir('./NewFlowTestCase')  # 将当前目录切换到 testcase/search_testcase 目录
# 指定测试用例为当前文件夹下的 testcase/search_testcase 目录
# test_dir = './testcase/search_testcase'
discover = unittest.defaultTestLoader.discover('./',pattern = 'test*.py')


if __name__ == "__main__":
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	filename = '../report/' + now + 'flowTestResult.html'
	fp = open(filename, 'wb')
	runner = HTMLTestRunner(stream=fp,
							title='发货宝系统接口流程自动化测试报告')
	runner.run(discover)
	#调用关闭数据库方法
	closedb(global_var.db, global_var.db1)
	fp.close()

