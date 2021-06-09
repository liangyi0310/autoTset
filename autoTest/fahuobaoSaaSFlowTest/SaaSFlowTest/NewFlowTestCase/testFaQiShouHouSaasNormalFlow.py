import unittest
import requests
import json
import datetime
import time
#导入公用参数readConfig.py
from Common.readConfig import *

class TestMethod(unittest.TestCase):    # 定义一个类，继承自unittest.TestCase
    '''发起售后流程测试'''
    def test_a(self):
        '''录单'''
        #录单接口
        url1 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        i = datetime.datetime.now()
        print("收件人姓名：发起售后测试" + str(i.month) + str(i.day))
        data1 = {
                "businessNo": "BSTE02",
                "serviceNo": "FHB01",
                "orderWay": 1,
                "wokerUserName": "",
                "wokerPhone": "",
                "wokerPrice": "",
                "checked": "",
                "verfiyType": "",
                "goods": [
                    {
                        "num": 1,
                        "picture": "J020800",
                        "memo": "产品描述XX",
                        "bigClassNo": "J02",
                        "middleClassNo": "J020800",
                        "pictureType": "1"
                    }
                ],
                "isElevator": "0",
                "predictServiceDate": "",
                "predictDevliveryDate": "",
                "memo": "",
                "isArriva": 1,
                "boolCollection": "0",
                "collectionMoney": "",
                "collectionMemo": "",
                "allVolume": "2",
                "allWeight": "12",
                "allPackages": "3",
                "allCargoPrice": "1212",
                "consigneeName": "发起售后测试" + str(i.month) + str(i.day),
                "consigneePhone": "15023621702",
                "consigneeAddress": "武侯大道",
                "floor": "2",
                "deliveryName": "提货联系:",
                "deliveryPhone": "15023621702",
                "provinceNo": "510000",
                "province": "四川省",
                "cityNo": "510100",
                "city": "成都市",
                "districtNo": "510107",
                "district": "武侯区",
                "deliveryProvinceNo": "",
                "deliveryProvince": "",
                "deliveryCityNo": "",
                "deliveryCity": "",
                "deliveryDistrictNo": "",
                "deliveryDistrict": "",
                "verifyOrderNo": ""
            }
        request1 = requests.post( url1, data = json.dumps(data1) ,headers = global_var.headers1)
        print("录单：" + request1.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request1.text, msg='测试fail')

    def test_b(self):
        '''连接数据库查询订单'''
        global i,consignee_name1
        i = datetime.datetime.now()
        consignee_name1 = "发起售后测试" + str(i.month) + str(i.day)
        # 使用cursor()方法获取操作游标
        cursor = global_var.db.cursor()
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
        '''师傅报价'''
        url2 = "http://" + global_var.api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data2 = {
                    "memo": "",
                    "money": "200",
                    "orderId": orderid
                }
        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=global_var.headers2)
        print("师傅报价：" + request2.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request2.text, msg='测试fail')

    def test_d(self):
        '''web端报价中选择师傅'''
        global_var.db.connect()
        sql2 = "select id from fhb_order_bidding_log where fhb_order_id = '" + orderid + "'"
        # 使用cursor()方法获取操作游标
        cursor2 = global_var.db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # 有多个的情况，取第一个订单的id
        biddinglogid = results2[0]['id']
        print("竞价记录id:" + biddinglogid)
        url3 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId=" + orderid + "&biddingLogId=" + biddinglogid + ""
        request3 = requests.get(url3, headers=global_var.headers1)
        print("选择师傅get请求的url:" + url3)
        print("选择师傅：" + request3.text)
        self.assertIn(global_var.arg1, request3.text, msg='测试fail')

    def test_e(self):
        '''数据库更新竞价金额为0.01'''
        # 数据库更新竞价金额为0.01
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = global_var.db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        # MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        global_var.db.commit()

    def test_f(self):
        '''钱包余额支付中标费用'''
        url4 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data4 = {
            "objectList": [orderid],
            "money": 0.01,
            "password": "123456"
        }
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=global_var.headers1)
        print("钱包余额支付中标费用：" + request4.text)
        time.sleep(6)
        self.assertIn(global_var.arg1, request4.text, msg='测试fail')

    def test_g(self):
        '''居家小二操作预约'''
        global_var.db1.connect()
        sql5 = "select id from order_data where order_no = '" + orderno + "'"
        print(sql5)
        # 使用cursor()方法获取操作游标
        cursor5 = global_var.db1.cursor()
        # 执行SQL语句
        cursor5.execute(sql5)
        global_var.db1.commit()
        # 获取所有记录列表
        results5 = cursor5.fetchall()
        # 有多个的情况，取第一个订单的id
        global xrid
        xrid = results5[0]['id']
        print("通过fhb订单号查询居家小二订单id:" + xrid)
        url5 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/appointappoint-distributionOne-choose"
        data5 = {
            "branchUserId": "",
            "cause": "",
            "codeYT": "night",
            "ids": [xrid],
            "timeYT": str(i.year) + "-" + str(i.month) + "-" + str(i.day)
        }
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=global_var.headers2)
        print("预约：" + request5.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request5.text, msg='测试fail')

    def test_h(self):
        '''居家小二操作提货'''
        global_var.db1.connect()
        sql6 = "select id from assign_worker where order_id = '" + xrid + "'"
        print(sql6)
        cursor6 = global_var.db1.cursor()
        cursor6.execute(sql6)
        # 获取所有记录列表
        results6 = cursor6.fetchall()
        # print(results6[0])
        assignid = results6[0]["id"]
        print("assigned:" + assignid)
        url6 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/pickGoods"
        data6 = {"assignId": assignid, "imgId": ["5b5810b5d423d400017bf0c2"], "serviceTypeCode": "CZSETE01"}
        request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=global_var.headers2)
        print("提货：" + request6.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request6.text, msg='测试fail')

    def test_i(self):
        '''商家追加费用'''
        url11 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/addfee-balance-pay"
        data11 = {
            "additionalName": "追加费",
            "additionalMoney": "0.01",
            "additionalMemo": "需要追加费用",
            "orderId": orderid,
            "password": "123456"
        }
        request11 = requests.request("POST", url=url11, data=json.dumps(data11), headers=global_var.headers1)
        print("追加费用：" + request11.text)
        time.sleep(1)
        self.assertIn(global_var.arg1, request11.text, msg='测试fail')

    def test_j(self):
        '''居家小二操作上门'''
        global_var.db1.connect()
        sql6 = "select id from assign_worker where order_id = '" + xrid + "'"
        print(sql6)
        cursor6 = global_var.db1.cursor()
        cursor6.execute(sql6)
        # 获取所有记录列表
        results6 = cursor6.fetchall()
        # print(results6[0])
        global assignid
        assignid = results6[0]["id"]
        print("assigned:" + assignid)
        url7 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/houseCall?assignId=" + assignid + "&orderId=" + assignid + ""
        request7 = requests.request("POST", url=url7, headers=global_var.headers2)
        print("上门：" + request7.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request7.text, msg='测试fail')

    def test_k(self):
        '''居家小二操作签收'''
        global_var.db.connect()
        sql8 = "select service_code from fhb_order where order_no = '" + orderno + "'"
        cursor8 = global_var.db.cursor()
        cursor8.execute(sql8)
        # 获取所有记录列表
        results8 = cursor8.fetchall()
        # print(results8[0])
        serviceCode = results8[0]["service_code"]
        print("serviceCode:" + serviceCode)
        url8 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/appOrderSign"
        data8 = {
            "assignId": assignid,
            "imgId": ["5b581a07d423d400017bf0d2"],
            "jdVerificationCode": "",
            "qmImg": "5b581a00d423d400017bf0d0",
            "serviceCode": serviceCode,
            "serviceTypeCode": "CZSETE01"
        }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=global_var.headers2)
        print("签收：" + request8.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request8.text, msg='测试fail')

    def test_l(self):
        '''发货宝确认评价'''
        url9 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/evaluation"
        data9 = {
            "fhbOrderId": orderid,
            "stars": 5,
            "pictures": "5b581cfbd423d400017bf0d4",
            "memo": "评价说明",
            "tips": "做事认真负责,技术超好,服务守时"
        }
        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=global_var.headers1)
        print("确认评价：" + request9.text)
        time.sleep(4)
        self.assertIn(global_var.arg1, request9.text, msg='测试fail')

    def test_m(self):
        '''运营管理进行订单结算'''
        url10 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/order-wallet/clearing-confirm"
        data10 = xrid
        request10 = requests.request("POST", url=url10, data=data10, headers=global_var.headers3)
        print("订单结算：" + request10.text)
        self.assertIn(global_var.arg1, request10.text, msg='测试fail')
        time.sleep(1)

    def test_n(self):
        '''发起售后'''
        url12 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrderAgain/initAfterSale"
        data12 = {"orderId": orderid}
        request12 = requests.request("POST",url=url12,data=data12,headers=global_var.headers1)
        print("发起售后: " + request12.text)
        self.assertIn(global_var.arg1, request12.text, msg='测试fail')
        time.sleep(1)

    def test_o(self):
        '''售后暂存单转正'''
        consignee_name2 = '""发起售后测试" + str(i.month) + str(i.day)"'
        # 使用cursor()方法获取操作游标
        cursor = global_var.db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql13 = "select id,order_no from fhb_order_temp where consigneeName = '" + consignee_name2 + "'  ORDER BY foundtime DESC"
        # 执行SQL语句
        cursor.execute(sql13)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global orderTempId, orderTempNo
        orderTempId = results[0]['id']
        orderTempNo1 = results[0]['order_no']
        #将带双引号的订单去除两端的双引号
        orderTempNo = eval(orderTempNo1)
        print("售后暂存订单id:" + orderTempId)
        print("售后订单编号:" + orderTempNo)
        data13 = {
                    "businessNo": "BSTE02",
                    "serviceNo": "FHB04",
                    "orderWay": 2,
                    "wokerUserName": "gxl",
                    "wokerPhone": "17608080803",
                    "wokerPrice": "0.01",
                    "checked": "",
                    "verfiyType": "",
                    "goods": [
                        {
                            "num": 1,
                            "picture": "J020800",
                            "memo": "产品描述XX",
                            "bigClassNo": "J02",
                            "middleClassNo": "J020800",
                            "pictureType": "1"
                        }
                    ],
                    "isElevator": "0",
                    "predictServiceDate": "",
                    "predictDevliveryDate": "",
                    "memo": "",
                    "isArriva": 1,
                    "boolCollection": "0",
                    "collectionMoney": "",
                    "collectionMemo": "",
                    "wokerPickMoney": "",
                    "allVolume": "2",
                    "allWeight": "12",
                    "allPackages": "3",
                    "allCargoPrice": "1212",
                    "consigneeName": "定向报价配装测试97",
                    "consigneePhone": "15023621702",
                    "floor": 2,
                    "consigneeAddress": "武侯大道",
                    "deliveryName": "提货联系:",
                    "deliveryPhone": "15023621702",
                    "deliveryAddress": "",
                    "deliveryMemo": "",
                    "provinceNo": "510000",
                    "province": "四川省",
                    "cityNo": "510100",
                    "city": "成都市",
                    "districtNo": "510107",
                    "district": "武侯区",
                    "deliveryProvinceNo": "",
                    "deliveryProvince": "",
                    "deliveryCityNo": "",
                    "deliveryCity": "",
                    "deliveryDistrictNo": "",
                    "deliveryDistrict": "",
                    "verifyOrderNo": "",
                    "id": orderTempId,
                    "orderNo": orderTempNo,
                    "inputType": "LRFS03"
            }
        url1 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        request13 = requests.post(url1, data=json.dumps(data13), headers=global_var.headers1)
        print("售后订单转正：" + request13.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request13.text, msg='测试fail')

    def test_p(self):
        '''售后订单师傅报价'''
        # 连接数据库查询订单
        # 使用cursor()方法获取操作游标
        cursor = global_var.db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql1 = "select id from fhb_order where id in (select fhb_order_id from fhb_order_consignee_info where consigne_name = '" + consignee_name1 + "') ORDER BY foundtime DESC"
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global shOrderId
        shOrderId = results[0]['id']
        print("售后订单id:" + shOrderId)

    def test_q(self):
        '''售后订单:师傅报价'''
        url2 = "http://" + global_var.api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data2 = {
            "memo": "",
            "money": "200",
            "orderId": shOrderId
        }
        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=global_var.headers2)
        print("师傅报价：" + request2.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request2.text, msg='测试fail')

    def test_r(self):
        '''售后订单:数据库更新竞价金额为0.01'''
        # 数据库更新竞价金额为0.01
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + shOrderId + "'"
        print(sql3)
        cursor3 = global_var.db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        # MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        global_var.db.commit()

    def test_s(self):
        '''售后订单:钱包余额支付中标费用'''
        url4 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data4 = {
            "objectList": [shOrderId],
            "money": 0.01,
            "password": "123456"
        }
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=global_var.headers1)
        print("钱包余额支付中标费用：" + request4.text)
        time.sleep(6)
        self.assertIn(global_var.arg1, request4.text, msg='测试fail')

    def test_t(self):
        '''售后订单:居家小二操作预约'''
        global_var.db1.connect()
        sql5 = "select id from order_data where order_no = '" + orderTempNo + "'"
        print(sql5)
        # 使用cursor()方法获取操作游标
        cursor5 = global_var.db1.cursor()
        # 执行SQL语句
        cursor5.execute(sql5)
        global_var.db1.commit()
        # 获取所有记录列表
        results5 = cursor5.fetchall()
        # 有多个的情况，取第一个订单的id
        global xrid1
        xrid1 = results5[0]['id']
        print("通过fhb订单号查询居家小二订单id:" + xrid1)
        url5 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/appointappoint-distributionOne-choose"
        data5 = {
            "branchUserId": "",
            "cause": "",
            "codeYT": "night",
            "ids": [xrid1],
            "timeYT": str(i.year) + "-" + str(i.month) + "-" + str(i.day)
        }
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=global_var.headers2)
        print("预约：" + request5.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request5.text, msg='测试fail')

    def test_u(self):
        '''售后订单:居家小二操作提货'''
        global_var.db1.connect()
        sql6 = "select id from assign_worker where order_id = '" + xrid1 + "'"
        print(sql6)
        cursor6 = global_var.db1.cursor()
        cursor6.execute(sql6)
        # 获取所有记录列表
        results6 = cursor6.fetchall()
        # print(results6[0])
        assignid1 = results6[0]["id"]
        print("assigned:" + assignid1)
        url6 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/pickGoods"
        data6 = {"assignId": assignid1, "imgId": ["5b5810b5d423d400017bf0c2"], "serviceTypeCode": "CZSETE01"}
        request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=global_var.headers2)
        print("提货：" + request6.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request6.text, msg='测试fail')

    def test_v(self):
        '''售后订单:商家追加费用'''
        url11 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/addfee-balance-pay"
        data11 = {
            "additionalName": "追加费",
            "additionalMoney": "0.01",
            "additionalMemo": "需要追加费用",
            "orderId": shOrderId,
            "password": "123456"
        }
        request11 = requests.request("POST", url=url11, data=json.dumps(data11), headers=global_var.headers1)
        print("追加费用：" + request11.text)
        time.sleep(1)
        self.assertIn(global_var.arg1, request11.text, msg='测试fail')

    def test_w(self):
        '''售后订单:居家小二操作上门'''
        global_var.db1.connect()
        sql6 = "select id from assign_worker where order_id = '" + xrid1 + "'"
        print(sql6)
        cursor6 = global_var.db1.cursor()
        cursor6.execute(sql6)
        # 获取所有记录列表
        results6 = cursor6.fetchall()
        # print(results6[0])
        global assignid1
        assignid1 = results6[0]["id"]
        print("assigned:" + assignid1)
        url7 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/houseCall?assignId=" + assignid1 + "&orderId=" + assignid + ""
        request7 = requests.request("POST", url=url7, headers=global_var.headers2)
        print("上门：" + request7.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request7.text, msg='测试fail')

    def test_x(self):
        '''售后订单:居家小二操作签收'''
        global_var.db.connect()
        sql8 = "select service_code from fhb_order where order_no = '" + orderTempNo + "'"
        cursor8 = global_var.db.cursor()
        cursor8.execute(sql8)
        # 获取所有记录列表
        results8 = cursor8.fetchall()
        # print(results8[0])
        serviceCode1 = results8[0]["service_code"]
        print("serviceCode:" + serviceCode1)
        url8 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/appOrder/appOrderSign"
        data8 = {
            "assignId": assignid1,
            "imgId": ["5b581a07d423d400017bf0d2"],
            "jdVerificationCode": "",
            "qmImg": "5b581a00d423d400017bf0d0",
            "serviceCode": serviceCode1,
            "serviceTypeCode": "CZSETE01"
        }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=global_var.headers2)
        print("签收：" + request8.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request8.text, msg='测试fail')

    def test_y(self):
        '''售后订单:发货宝确认评价'''
        url9 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/evaluation"
        data9 = {
            "fhbOrderId": shOrderId,
            "stars": 5,
            "pictures": "5b581cfbd423d400017bf0d4",
            "memo": "评价说明",
            "tips": "做事认真负责,技术超好,服务守时"
        }
        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=global_var.headers1)
        print("确认评价：" + request9.text)
        time.sleep(4)
        self.assertIn(global_var.arg1, request9.text, msg='测试fail')

    def test_z(self):
        '''售后订单:运营管理进行订单结算'''
        url10 = "http://" + global_var.api_host + "/ms-fahuobao-order-data/order-wallet/clearing-confirm"
        data10 = xrid1
        request10 = requests.request("POST", url=url10, data=data10, headers=global_var.headers3)
        print("订单结算：" + request10.text)
        self.assertIn(global_var.arg1, request10.text, msg='测试fail')


if __name__ == "__main__":
    unittest.main()