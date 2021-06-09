# -*- coding: utf-8 -*-

import requests
import json
import datetime
import time
import unittest
from Common.readConfig import *

api_host=global_var.api_host #测试地址：192.168.10.56
headers1=global_var.headers4 #发货宝18883612485
headers2=global_var.headers5 #小二18599937985
headers3=global_var.headers6 #运营后台18883612485
headers4=global_var.headers7 #直营系统18883612485
headersNull=global_var.headersNull #居家小二客户端18883612485
goods=global_var.goods
db=global_var.db #数据库 59
db1=global_var.db1 #数据库70
arg1=global_var.arg1 #断言文本
Pictureid = '5b4ef81bd423d40001f0195e' #图片id


class testTuiKuanFlow(unittest.TestCase):
    print("执行退款流程测试-关闭订单")
    def test_a(self):
        '''录单'''
        url1 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        i = datetime.datetime.now()
        print("收件人姓名：退款流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))

        data1 = {
                "businessNo": "BSTE02",
                "serviceNo": "FHB01",
                "orderWay": "1",
                "wokerUserName": "",
                "wokerPhone": "",
                "wokerPrice": "",
                "checked": "",
                "verfiyType": "",
                "goods": goods,
                "isElevator": "",
                "predictServiceDate": "",
                "predictDevliveryDate": "",
                "memo": "",
                "isArriva": 1,
                "boolCollection": "0",
                "collectionMoney": "",
                "collectionMemo": "",
                "allVolume": "1",
                "allWeight": "1",
                "allPackages": "1",
                "consigneeName": "退款流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute),
                "consigneePhone": "18883612485",
                "consigneeAddress": "231",
                "deliveryName": "23213",
                "deliveryPhone": "18883612485",
                "provinceNo": "430000",
                "province": "湖南省",
                "cityNo": "430100",
                "city": "长沙市",
                "districtNo": "430103",
                "district": "天心区",
                "deliveryProvinceNo": "",
                "deliveryProvince": "",
                "deliveryCityNo": "",
                "deliveryCity": "",
                "deliveryDistrictNo": "",
                "deliveryDistrict": "",
                "verifyOrderNo": ""
            }


        request1 = requests.request("POST", url=url1, data = json.dumps(data1) ,headers = headers1)
        print("录单：" + request1.text)
        time.sleep(3)
        self.assertIn(arg1, request1.text, msg='测试fail')

    def test_b(self):
        '''查询id、订单编号'''
        # 打开数据库连接 ,db为59数据库,db1为70数据库
        global i
        i = datetime.datetime.now()
        consignee_name1 = "退款流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql1 = "select id,order_no from fhb_order where id in (select fhb_order_id from fhb_order_consignee_info where consigne_name = '" + consignee_name1 + "') ORDER BY foundtime DESC"
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global orderid, orderno
        orderid = results[0]['id']
        orderno = results[0]['order_no']
        print("订单id:" + orderid)
        print("订单编号:" + orderno)

    def test_c(self):
        # print('竞价')
        # 将订单推到天心区并用185这个账号进行竞价
        '''将订单推到天心区并用185这个账号进行竞价'''
        url2 = "http://" +  api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data2 = {
                "memo":"",
                "money":"200",
                "orderId":orderid
            }

        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers2)
        print("竞价：" + request2.text)
        time.sleep(2)
        self.assertIn(arg1,request2.text,msg='测试faild')
    def test_d(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        global_var.db.connect()
        sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = global_var.db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global fhb_order_id,jingjiaid
        fhb_order_id=orderid
        jingjiaid = results2[0]['id']
        print("订单id:" + fhb_order_id)
        print("竞价id:" + jingjiaid)
        # db.close()
        time.sleep(2)
    def test_e(self):
        # 修改竞价金额为0.01
        '''修改竞价金额为0.01'''
        # db.connect()
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()
    def test_f(self):
        # 选择师傅接口
        '''选择师傅'''
        url3="http://" +  api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId="+fhb_order_id+"&biddingLogId="+jingjiaid+""
        request3 = requests.request("GET", url=url3, headers=headers1)
        time.sleep(2)
        self.assertIn(arg1,request3.text,msg='测试filed')
    def test_g(self):
        # 支付接口，objectList为订单id
        '''支付'''
        time.sleep(5)
        url4 = "http://" +  global_var.api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data4 = {"objectList":[fhb_order_id],"money":0.01,"password":"123456"}
        # print(data4)
        # print(json.dumps(data4))
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("支付：" + request4.text)
        time.sleep(2)
        self.assertIn(arg1,request4.text,msg='测试filed')
    def test_h(self):
        # 发起退款
        '''发起退款'''
        url5 = "http://" +  api_host + "/ms-fahuobao-order/merRefund/saveOrderRefundRecord"
        data5 = {"refundAmount": "0.01", "refundMemo": "", "refundPic": "", "refundOrderState": 1, "orderId": fhb_order_id}
        # print(data5)
        # print(json.dumps(data5))
        time.sleep(2)
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers1)
        print("发起退款：" + request5.text)
        time.sleep(2)
        self.assertIn(arg1, request5.text, msg='测试filed')
    def test_i(self):
        # 师傅不同意转仲裁
        '''师傅不同意转仲裁'''
        url6 = "http://" +  global_var.api_host + "/ms-fahuobao-order/merRefund/saveAuditOrderRefundRecord"
        data6 = {
            "memo":"951",
            "state":1,
            "picture":[
                "5b4ef81bd423d40001f0195e"
            ],
            "orderId":fhb_order_id
        }

        request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=headers2)
        print("不同意转仲裁：" + request6.text)
        time.sleep(2)
        self.assertIn(arg1, request6.text, msg='测试filed')
    def test_j(self):
        # 仲裁处理
        '''仲裁处理'''
        url7 = "http://" +  global_var.api_host + "/ms-fahuobao-order/merRefund/saveArbitrateOrderRefundRecord"
        data7 = {
                "arbitrateAmount":"0.01",
                "arbitratePic":"5b4ef81bd423d40001f0195e",
                "arbitrateMemo":"32132",
                "orderId":fhb_order_id
            }
        request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers3)
        print("仲裁处理：" + request7.text)
        time.sleep(2)
        self.assertIn(global_var.arg1, request7.text, msg='测试filed')
    def test_k(self):
        #查询发货宝订单状态
        # 使用cursor()方法获取操作游标
        '''查询发货宝订单状态'''
        cursor = db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql4 = "select order_status from fhb_order where id ='"+fhb_order_id+"'"
        # 执行SQL语句
        cursor.execute(sql4)
        # 获取所有记录列表
        results4 = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        order_status = results4[0]['order_status']
        print("发货宝订单状态:" + order_status)
        if self.assertEqual(order_status,'close|0')==None:
            print("订单确认以关闭:"+orderno)
        else:
            print("测试失败:%s" %(orderno))




if __name__ == '__main__':
    unittest.main()