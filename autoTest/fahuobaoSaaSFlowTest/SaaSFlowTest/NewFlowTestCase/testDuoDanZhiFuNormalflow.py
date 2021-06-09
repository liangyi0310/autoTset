# -*- coding: utf-8 -*-

import requests
import json
import datetime
import time
import unittest
from Common.readConfig import *

# 发货宝web端操作用户18883612485，headers1发货宝用户,headers2小二用户

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


class testDuoDanZhiFuFlow(unittest.TestCase):
    # 发货宝录单接口
    def test_a(self):
        '''录单'''
        url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        i = datetime.datetime.now()
        print("收件人姓名：多单支付测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))
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
                    "consigneeName": "多单支付测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute),
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
        num=0
        while num<3:
            request1 = requests.request("POST", url=url1, data = json.dumps(data1) ,headers = headers1)
            print("录单：" + request1.text)
            self.assertIn(arg1, request1.text, msg='测试field')
            time.sleep(1)
            num+=1

    def test_b(self):
        '''查询出订单fhb_order_id'''
        i = datetime.datetime.now()
        consigne_name1 = "多单支付测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)
        time.sleep(2)
        # 通过订单的收件人姓名查询出订单id
        sql1 = "SELECT fhb_order_id FROM fhb_order_consignee_info WHERE consigne_name like '"+consigne_name1+"' ORDER BY foundtime DESC "
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id，分批次取出订单id
        global orderid,orderid1,orderid2
        orderid = results[0]['fhb_order_id']
        orderid1 = results[1]['fhb_order_id']
        orderid2 = results[2]['fhb_order_id']
        # servicecode=results[0]['service_code']
        # orderno = results[0]['order_no']
        print("订单id:" + orderid +"订单id1:" + orderid1+"订单id2:" + orderid2)
        # print("订单id1:" + orderid1)
        # print("订单id2:" + orderid2)
        # print("订单编号:" + orderno)
        time.sleep(1)
        db.close()
    def test_c(self):
        # 将订单推到天心区并用185这个账号进行竞价
        '''竞价'''
        url2 = "http://" +  api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data2 = {
                "memo":"",
                "money":"200",
                "orderId":orderid
            }
        data2_1 = {
            "memo": "",
            "money": "200",
            "orderId": orderid1
        }
        data2_2 = {
            "memo": "",
            "money": "200",
            "orderId": orderid2
        }

        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers2)
        print("竞价：" + request2.text)
        self.assertIn(arg1, request2.text, msg='测试field')
        time.sleep(1)
        request2_1 = requests.request("POST", url=url2, data=json.dumps(data2_1), headers=headers2)
        print("竞价1：" + request2_1.text)
        self.assertIn(arg1, request2_1.text, msg='测试field')
        time.sleep(1)
        request2_2 = requests.request("POST", url=url2, data=json.dumps(data2_2), headers=headers2)
        print("竞价2：" + request2_2.text)
        self.assertIn(arg1, request2_2.text, msg='测试field')

    def test_d(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        db.connect()
        time.sleep(2)
        sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f'  and fhb_order_id='"+orderid+"' order by foundtime desc"
        # sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='1474d9aa-c17a-4bd2-b1de-6823e873d4a5'  and fhb_order_id='" + orderid + "' order by foundtime desc"

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
        db.close() #关闭数据库
    def test_e(self):
        # 通过师傅id查询竞价记录
        '''修改竞价金额'''
        db.connect()
        time.sleep(2)
        sql3 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f'  and fhb_order_id='"+orderid1+"' order by foundtime desc"
        # sql3 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='1474d9aa-c17a-4bd2-b1de-6823e873d4a5'  and fhb_order_id='" + orderid + "' order by foundtime desc"
        # 使用cursor()方法获取操作游标
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        # 获取所有记录列表
        results3 = cursor3.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global fhb_order_id1,jingjiaid1
        fhb_order_id1=orderid1
        jingjiaid1 = results3[0]['id']
        print("订单id1:" + fhb_order_id1)
        print("竞价id1:" + jingjiaid1)
        db.close() #关闭数据库
    def test_f(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        db.connect()
        time.sleep(2)
        sql4 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f'  and fhb_order_id='"+orderid2+"' order by foundtime desc"
        # sql4 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='1474d9aa-c17a-4bd2-b1de-6823e873d4a5'  and fhb_order_id='" + orderid + "' order by foundtime desc"
        # 使用cursor()方法获取操作游标
        cursor4 = db.cursor()
        # 执行SQL语句
        cursor4.execute(sql4)
        # 获取所有记录列表
        results4 = cursor4.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global fhb_order_id2,jingjiaid2
        fhb_order_id2=orderid2
        jingjiaid2 = results4[0]['id']
        print("订单id2:" + fhb_order_id2)
        print("竞价id2:" + jingjiaid2)
        # db.close()
    def test_g(self):
        # 修改竞价金额为0.01
        '''修改竞价金额'''
        sql5 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id in('" + orderid + "','"+orderid1+"','"+orderid2+"')"
        print(sql5)
        cursor5 = db.cursor()
        # 执行SQL语句
        cursor5.execute(sql5)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()
    def test_h(self):
        # 选择接口
        '''选择师傅'''
        time.sleep(2)
        url3 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId="+fhb_order_id+"&biddingLogId="+jingjiaid+""
        time.sleep(0.5)
        url3_1 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId=" + fhb_order_id1 + "&biddingLogId=" + jingjiaid1 + ""
        time.sleep(0.5)
        url3_2 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId=" + fhb_order_id2 + "&biddingLogId=" + jingjiaid2 + ""
        request_duodanzhifu = requests.request("GET", url=url3, headers=headers1)
        self.assertIn(arg1, request_duodanzhifu.text, msg='测试field')
        time.sleep(2)
        request_duodanzhifu1 = requests.request("GET", url=url3_1, headers=headers1)
        self.assertIn(arg1, request_duodanzhifu1.text, msg='测试field')
        time.sleep(2)
        request_duodanzhifu2 = requests.request("GET", url=url3_2, headers=headers1)
        self.assertIn(arg1, request_duodanzhifu2.text, msg='测试field')
        time.sleep(2)

    def test_i(self):
        # 支付接口，objectList为订单id
        '''订单支付'''
        url4 = "http://" +  api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data4 = {"objectList":[fhb_order_id,fhb_order_id1,fhb_order_id2],"money":0.03,"password":"123456"}
        # print(json.dumps(data4))
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("多单支付：" + request4.text)
        self.assertIn(arg1, request4.text, msg='测试field')



if __name__ == '__main__':
    unittest.main()
