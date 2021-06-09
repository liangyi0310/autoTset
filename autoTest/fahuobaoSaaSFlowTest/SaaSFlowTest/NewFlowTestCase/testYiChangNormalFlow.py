# -*- coding: utf-8 -*-

import requests
import pymysql
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

# 录单使用的产品信息


class testYiChangFlow(unittest.TestCase):
    def test_a(self):
        '''录单'''
        #发货宝录单接口
        url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        global i
        i = datetime.datetime.now()
        print("收件人姓名：异常流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))
        data1 =  {
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
                "consigneeName": "异常流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute),
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
        time.sleep(2)
        self.assertIn(arg1, request1.text, msg='测试field')

    def test_b(self):
        '''通过订单的收件人姓名查询出订单id、订单编号,将订单推到天心区并用185这个账号进行竞价'''
        i = datetime.datetime.now()
        consigne_name1 = "异常流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)

        # 通过订单的收件人姓名查询出订单id
        sql1 = "SELECT fhb_order_id,order_no FROM fhb_order_consignee_info a inner join  fhb_order b on a.fhb_order_id=b.id WHERE a.consigne_name = '"+consigne_name1+"' ORDER BY a.foundtime DESC"

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global orderid,orderno
        orderid = results[0]['fhb_order_id']
        orderno = results[0]['order_no']
        print("订单id:" + orderid)
        print("订单编号:" + orderno)
        db.close()
        # 将订单推到天心区并用185这个账号进行竞价
        url2 = "http://" +  api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data2 = {
                "memo":"",
                "money":"200",
                "orderId":orderid
            }

        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers2)
        print("竞价：" + request2.text)
        self.assertIn(arg1, request2.text, msg='测试field')
    def test_c(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        db.connect()
        sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = db.cursor()
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
    def test_d(self):
        # 修改竞价金额为0.01
        '''修改竞价金额为0.01'''
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()
    def test_e(self):
        # 选择接口
        '''选择师傅'''
        url3 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId="+fhb_order_id+"&biddingLogId="+jingjiaid+""
        request_yichang = requests.request("GET", url=url3, headers=headers1)
        # print('选择中标师傅'+request_yichang.text)
        time.sleep(2)
        self.assertIn(arg1, request_yichang.text, msg='测试field')


    def test_f(self):
        # 支付接口，objectList为订单id
        '''支付'''
        time.sleep(5)
        url4 = "http://" +  api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data4 = {"objectList":[fhb_order_id],"money":0.01,"password":"123456"}
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("支付：" + request4.text)
        time.sleep(2)
        self.assertIn(arg1, request4.text, msg='测试field')


        # 通过发货宝订单编号查出scm订单id与订单编号
    def test_g(self):
        '''通过发货宝订单编号查出scm订单id与订单编号'''
        time.sleep(5)
        db1.connect()
        sql4 = "select id,order_no from order_data where order_no='"+orderno+"'"

        # 使用cursor()方法获取操作游标
        cursor3 = db1.cursor()
        # 执行SQL语句
        cursor3.execute(sql4)
        # 获取所有记录列表
        results3 = cursor3.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global scmorderid,scmorderno
        scmorderid = results3[0]['id']
        scmorderno=results3[0]['order_no']
        print("scm订单id:" + scmorderid)
        print("scm订单编号:" + scmorderno)

        # db2.close()
    def test_h(self):
        # 预约
        '''预约'''
        url5 = "http://" +  api_host + "/ms-fahuobao-order-data/appOrder/appointappoint-distributionOne-choose"
        data5 = {
                    "branchUserId": "",
                    "cause": "",
                    "codeYT": "night",
                    "ids": [scmorderid],
                    "timeYT": str(i.year) + "-" + str(i.month) + "-" + str(i.day)
                }
        # print(json.dumps(data5))
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers2)
        print("预约：" + request5.text)
        time.sleep(2)
        self.assertIn(arg1, request5.text, msg='测试field')
    def test_i(self):
        # 师傅发起异常
        '''师傅发起异常'''
        Pictureid='5b4ef81bd423d40001f0195e'
        url6 = "http://" +  api_host + "/ms-fahuobao-order/fhbAbnormal/saveAbnormal"
        data6 = {
                "trunkPicture":[
                    Pictureid
                ],
                "isPickUp":1,
                "abnormalCode":"EXE02",
                "abnormalPicture":[
                    Pictureid
                ],
                "abnormalMemo":"",
                "abnormalPacks":"1",
                "orderId":scmorderid
            }

        request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=headers2)
        print("师傅发起异常：" + request6.text)
        time.sleep(2)
        self.assertIn(arg1, request6.text, msg='测试field')

    def test_j(self):
        # 通过订单id查出异常id
        '''通过订单id查出异常id'''
        time.sleep(5)
        db.connect()
        sql5 = "SELECT id FROM fhb_order_abnormal WHERE order_id ='"+orderid+"'  ORDER BY found_date DESC"

        # 使用cursor()方法获取操作游标
        cursor5 = db.cursor()
        # 执行SQL语句
        cursor5.execute(sql5)
        # 获取所有记录列表
        results5 = cursor5.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global yichangid
        yichangid = results5[0]['id']
        print("异常id:" + yichangid)
    def test_k(self):
        # 货主给出方案
        '''货主给出方案'''
        url7 = "http://" +  api_host + "/ms-fahuobao-order-abnormal/FhbOrderAbnormal/merProvideScheme"
        data7 = {
                "schemeDesc":"231321",
                "pic":[
                    Pictureid
                ],
                "id":yichangid
            }
        request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers1)
        print("货主给出方案：" + request7.text)
        time.sleep(2)
        self.assertIn(arg1, request7.text, msg='测试field')
    def test_l(self):
        # 师傅不同意货主方案（发起仲裁）
        '''师傅不同意货主方案（发起仲裁）'''
        url8 = "http://" +  api_host + "/ms-fahuobao-order-abnormal/FhbOrderAbnormal/workerApplyArbitration"
        data8 = {
                    "pic":[
                        Pictureid
                    ],
                    "schemeDesc":"321",
                    "id":yichangid
                }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=headers2)
        print("师傅不同意货主方案（发起仲裁）：" + request8.text)
        time.sleep(2)
        self.assertIn(arg1, request8.text, msg='测试field')
    def test_m(self):
        # 仲裁处理
        '''仲裁处理'''
        url9 = "http://" + api_host + "/ms-fahuobao-order-abnormal/FhbOrderAbnormal/dealArbitration"
        data9 ={"schemeDesc":"3131","refundAmount":"0.00","pic":[Pictureid],"refundOrderState":1,"id":yichangid}
        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=headers3)
        print("仲裁处理：" + request9.text)
        time.sleep(2)
        self.assertIn(arg1, request9.text, msg='测试field')


if __name__ == '__main__':
    unittest.main()
