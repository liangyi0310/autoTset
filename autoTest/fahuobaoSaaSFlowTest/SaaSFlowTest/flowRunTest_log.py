import logging,logging.handlers
import os
import datetime
import time

now=datetime.datetime.now()
logtime=str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
logdir=os.chdir('./logging')
print(os.getcwd())

#获取logger
logger=logging.getLogger('TestLog')
#设置logger级别
logger.setLevel(logging.INFO)
#设置logger格式
format_str=logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
#输出到控制台
st=logging.StreamHandler()
st.setFormatter(format_str)
#输出到文件
th=handlers.TimedRotatingFileHandler('TestLog.log',when='h',interval=2,encoding='utf-8')
th.setFormatter(format_str)
#添加到handler
logger.addHandler(st)
logger.addHandler(th)

logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')

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

# 修改日志文件名
filepath=os.chdir('../logging')
print(os.getcwd())
for a in os.listdir(filepath):
    if a=='TestLog.log':
        newname=str(logtime)+str(a)
        os.rename('./'+str(a),'./'+str(newname))
    else:
        pass

