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
goods=global_var.goods
Pictureid = '5b4ef81bd423d40001f0195e' #图片id



class testTouSuFlow(unittest.TestCase):
    def test_a(self):
        #发货宝录单接口
        '''录单'''
        url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        global i
        i = datetime.datetime.now()
        print("收件人姓名：取消订单流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))

        data1 =        {
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
                "consigneeName": "取消订单流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute),
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
        self.assertIn(arg1,request1.text,msg='测试field')

    def test_b(self):
        '''查询订单id、订单编号、服务码'''
        i = datetime.datetime.now()
        consigne_name1 = "取消订单流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)
        # 通过订单的收件人姓名查询出订单id
        db.connect()
        time.sleep(2)
        sql1 = "SELECT fhb_order_id,order_no,service_code FROM fhb_order_consignee_info a inner join  fhb_order b on a.fhb_order_id=b.id WHERE a.consigne_name = '"+consigne_name1+"' ORDER BY a.foundtime DESC"

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
        orderno=results[0]['order_no']
        # service_code=results[0]['service_code']
        print("订单id:" + orderid)
        print("订单编号:" + orderno)
        # print("服务码:" + service_code)
        db.close()
    def test_c(self):
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
        self.assertIn(arg1, request2.text, msg='测试field')
    def test_d(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        db.connect()
        sql2 = "SELECT id,fhb_order_id,people_user_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global fhb_order_id,jingjiaid,jingjiashifuid
        fhb_order_id=orderid
        jingjiaid = results2[0]['id']
        jingjiashifuid=results2[0]['people_user_id']
        print("订单id:" + fhb_order_id)
        print("竞价id:" + jingjiaid)
        print("竞价师傅id:" + jingjiashifuid)
        db.close()
    def test_e(self):
        '''修改竞价金额为0.01'''
        time.sleep(2)
        db.connect()
        # 修改竞价金额为0.01
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()

    def test_f(self):
        # 选择接口
        '''选择师傅'''
        url3 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId=" + fhb_order_id + "&biddingLogId=" + jingjiaid + ""
        request_xuanze = requests.request("GET", url=url3, headers=headers1)
        response=request_xuanze.json()
        people=response['data']['fhbOrderBiddingLogs'][0]['people']
        peopleUserPhone=response['data']['fhbOrderBiddingLogs'][0]['peopleUserPhone']
        peopleUserId=response['data']['fhbOrderBiddingLogs'][0]['peopleUserId']
        print("选择师傅为："+people+'-电话为'+peopleUserPhone+'userId为-'+peopleUserId)
        time.sleep(2)
        self.assertIn(arg1, request_xuanze.text, msg='测试field')

    def test_g(self):
        # 待付款取消订单
        '''待付款取消订单'''
        print("待付款取消订单")
        url4 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/cancelOrderData"
        data4 = {"reason":"订单信息填写错误，需重新下单","orderId":[orderid]}
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("取消订单-待付款：" + request4.text)
        time.sleep(2)
        self.assertIn(arg1, request4.text, msg='测试field')

    def test_h(self):
        # 竞价中取消订单
        '''竞价中取消订单'''
        print("竞价中取消订单")
        self.test_a()
        self.test_b()
        self.test_c()
        self.test_e()
        url5 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/cancelOrderData"
        data5 = {"reason": "订单信息填写错误，需重新下单", "orderId": [orderid]}
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers1)
        print("取消订单-竞价中：" + request5.text)
        time.sleep(2)
        self.assertIn(arg1, request5.text, msg='测试field')