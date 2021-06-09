# -*- coding: utf-8 -*-

import requests
import json
import datetime
import time
import unittest
from Common.operation_excle import *
from Common.readConfig import *

# 发货宝web端操作用户18883612485，headers1发货宝用户,headers2小二用户
api_host=global_var.api_host #测试地址：192.168.10.56
headers1=global_var.headers4 #发货宝18883612485
headers2=global_var.headers5 #小二18599937985
headers3=global_var.headers6 #运营后台18883612485
headers4=global_var.headers7 #直营系统18883612485
headersNull=global_var.headersNull #居家小二客户端18883612485
headersFromData=global_var.headersFormData #文件上传专用header
goods=global_var.goods
db=global_var.db #数据库 59
db1=global_var.db1 #数据库70
arg1=global_var.arg1 #断言文本
Pictureid = '5b4ef81bd423d40001f0195e' #图片id


class testDingDanChiNormal(unittest.TestCase):
    def setUp(self):
        '''导入前修改excle中的数据'''
        self.ope=OperationExcle('../excle/orderTemp.xls',0)
        #获取excle所有有效行数
        rows_count=self.ope.get_lines()
        for i in range(1,rows_count):
            #获取excle中的phone
            data_phone=self.ope.get_row_values(i)
            # print(int(data_phone[13]))
            #定义修改后的数据
            new_data_phone=int(data_phone[13])+1
            #phone所在列
            col_num=13
            #写入修改后的数据至excle
            self.ope.write_value(i,col_num,new_data_phone)
    #导入订单
    def test_a(self):
        '''导入订单'''
        fp=open('../excle/orderTemp.xls','rb')
        filepath={"file":(fp)} #上传文件时应加入参数'rb'，否则或报错：UnicodeDecodeError
        url1="http://" +  api_host + "/zuul/ms-common-excelupload/excel/fileImport?fileType=form-data"
        request1 = requests.request("POST", url=url1,files=filepath, headers= headersFromData)
        time.sleep(2)
        fp.close()
        print("订单导入：" + request1.text)
        self.assertIn(arg1, request1.text, msg='测试field')
    #查询暂存单订单
    def test_b(self):
        '''查询导入记录'''
        db.connect()
        time.sleep(2)
        sql1 = " select id,orderId, orderNo from fhb_order_temp where founder in (select id from fhb_user where phone='18883612485') and state = '1' and orderType = '1' ORDER BY found_date desc limit 5"
        # 使用cursor()方法获取操作游标
        cursor1 = db.cursor()
        # 执行SQL语句
        cursor1.execute(sql1)
        # 获取所有记录列表
        results1 = cursor1.fetchall()
        count=len(results1[::]) #
        global datas,list_id
        list_id=[]
        str1=","
        for i in range(count):
            id=results1[i]['id']
            # 返回orderId、orderNo格式为"value",用eval方法转换为可用的value
            orderId=eval(results1[i]['orderId'])
            orderNo=eval(results1[i]['orderNo'])
            print('暂存单id为：'+id+'暂存单订单id为：'+orderId+"暂存单订单编号为："+orderNo)
            list_id.append(id)
        datas=str1.join(list_id) #将list_id拼接为字符串作为data传参


    #删除暂存单订单
    def test_c(self):
        '''删除暂存单订单'''
        url1= "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/deleteOrder"
        data1 = {"orderIds":datas}
        print(json.dumps(data1))
        request1 = requests.request("POST", url=url1, data=json.dumps(data1), headers=headers1)
        print("删除暂存单订单：" + request1.text)
        self.assertIn(arg1, request1.text, msg='测试field')
        time.sleep(0.5)
        db.connect()
        time.sleep(2)
        sql2 = " select orderNo,orderId,state from fhb_order_temp where id in('"+datas+"') "
        # 使用cursor()方法获取操作游标
        cursor2 = db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        count2=len(results2[::])
        state_list=[]
        for i in range(count2):
            state=results2[i]['state']
            # 返回orderId、orderNo格式为"value",用eval方法转换为可用的value
            orderId=eval(results2[i]['orderId'])
            orderNo=eval(results2[i]['orderNo'])
            print('暂存单state为：'+state+'暂存单订单id为：'+orderId+"暂存单订单编号为："+orderNo)
            if self.assertEqual(state,0)==None:
                print("已确认暂存单%S被删除"%orderNo)
            else:
                print("订单删除失败%s,暂存单状态为%s"%(orderNo,state))

    #批量转正
    def test_d(self):
        '''批量转正'''
        self.test_b() #执行前调用test_b方法，完成要批量转正的订单查询
        time.sleep(2)
        url2= "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveBathOrder"
        data2 ={"ids":list_id}
        print(json.dumps(data2))
        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers1)
        print("批量转正：" + request2.text)
        self.assertIn(arg1, request2.text, msg='测试field')
        time.sleep(0.5)
        db.connect()
        sql3 = " select order_no,order_status from fhb_order where id in('"+datas+"') "
        # 使用cursor()方法获取操作游标
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        # 获取所有记录列表
        results3 = cursor3.fetchall()
        count2=len(results3[::])
        orderstatus_list=[]
        for i in range(count2):
            orderNo=results3[i]['order_no']
            order_status=results3[i]['order_status']
            print('订单编号为：'+orderNo+"订单节点状态为："+order_status)
            if self.assertEqual(order_status,'report|100')==None:
                print("已确认暂存单转正:%S,订单节点为%s"%(orderNo,order_status))
            else:
                print("订单转正失败%s,节点状态为%s"%(orderNo,order_status))