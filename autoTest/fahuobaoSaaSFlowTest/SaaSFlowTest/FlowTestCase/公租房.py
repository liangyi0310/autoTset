# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import datetime
import time

# web端操作用户
headers1 = {
            'Referer' : 'http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/applicationresultdetail/24'
}
arg1 = "两室一厅"
arg2 = "大竹林"
arg3 = "鸳鸯"
arg4 = "华岩"
arg5 = "茶园"
arg6 = "龙州湾"
arg7 = "井口-美丽阳光家园"
arg8 = "南岸区-江南水岸"
arg9 = "蔡家"
arg10 = "钓鱼嘴-半岛逸景●乐园"
arg11 = "碚都佳园"
arg12 = "龙洲南苑"
arg13 = "西永"
arg14 = "木耳"
arg15 = "界石"
arg16 = "陈家桥-学府悦园"
arg17 = "缙云新居"


def gongzu():
    count = 1
    while (count < 4):
        request1 = requests.request("POST", url="http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/getSqshjgAction"
                                    "?isInit=true&prefix=&pageNumber=" + str(count) + "&xm=&cnumber=&sqpq=&code=&tableName=QUERY25",headers= headers1)
        # print(request1.url)
        print("第"+ str(count) +"页:" + request1.text)
        # i = 0
        # self.assertIn(arg1, request1.text, msg = "no")
        time.sleep(1)
        count = count + 1



def main():
    gongzu()

if __name__ == '__main__':
    main()


