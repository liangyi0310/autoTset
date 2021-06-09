import unittest
import requests
import json
import datetime
import time
#导入公用参数readConfig.py
from Common.readConfig import *

class TestMethod(unittest.TestCase):    # 定义一个类，继承自unittest.TestCase
    '''支付审批流程测试'''
    def test_a(self):
        '''录单'''
        #录单接口
        url1 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        i = datetime.datetime.now()
        print("收件人姓名：yi支付审批" + str(i.month) + str(i.day))
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
                "consigneeName": "yi支付审批" + str(i.month) + str(i.day),
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
        count = 0
        while (count < 3):
            request1 = requests.request("POST", url=url1, data=json.dumps(data1), headers=global_var.headers1)
            print("录单：" + request1.text)
            time.sleep(2)
            self.assertIn(global_var.arg1, request1.text, msg='测试fail')
            count = count + 1

    def test_b(self):
        '''连接数据库查询订单'''
        global i
        i = datetime.datetime.now()
        global consignee_name1
        consignee_name1 = "yi支付审批" + str(i.month) + str(i.day)
        # 使用cursor()方法获取操作游标
        cursor = global_var.db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql1 = "select id,order_no from fhb_order where id in (select fhb_order_id from fhb_order_consignee_info where consigne_name like '%" + consignee_name1 + "%') ORDER BY foundtime DESC"
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global orderid1,orderid2,orderid3,orderno1,orderno2,orderno3
        orderid1 = results[0]['id']
        orderid2 = results[1]['id']
        orderid3 = results[2]['id']
        orderno1 = results[0]['order_no']
        orderno2 = results[1]['order_no']
        orderno3 = results[2]['order_no']

        print("第一个订单id:" + orderid1 + "第二个订单id:" + orderid2 + "第三个订单id:" + orderid3)
        print("第一个订单编号:" + orderno1 + "第二个订单编号:" + orderno2 + "第三个订单编号:" + orderno3)

    def test_c(self):
        '''师傅报价'''
        url2 = "http://" + global_var.api_host + "/ms-fahuobao-order/bidding/quoted-price"
        count1 = 0
        global orderid
        orderid = [orderid1, orderid2, orderid3]
        while count1 < 3:
            data2 = {
                "memo": "",
                "money": "200",
                "orderId": orderid[count1]
            }
            request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=global_var.headers2)
            print("师傅报价：" + request2.text)
            time.sleep(1)
            self.assertIn(global_var.arg1, request2.text, msg='测试fail')
            count1 = count1 + 1

    def test_d(self):
        '''web端报价中选择师傅'''
        global_var.db.connect()
        sql2 = "select id from fhb_order_bidding_log where fhb_order_id in (select fhb_order_id from fhb_order_consignee_info where consigne_name like '%" + consignee_name1 + "%') ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = global_var.db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # 有多个的情况，取第一个订单的id
        biddinglogid1 = results2[0]['id']
        biddinglogid2 = results2[1]['id']
        biddinglogid3 = results2[2]['id']
        print("第一个竞价记录id:" + biddinglogid1 + "第二个竞价记录id:" + biddinglogid1 + "第三个竞价记录id:" + biddinglogid1)
        count3 = 0
        biddinglogid = [biddinglogid1, biddinglogid2, biddinglogid3]
        while count3 < 3:
            url3 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId=" + orderid[
                count3] + "&biddingLogId=" + biddinglogid[count3] + ""
            request3 = requests.get(url3, headers=global_var.headers1)
            print("选择师傅：" + request3.text)
            time.sleep(1)
            self.assertIn(global_var.arg1, request3.text, msg='测试fail')
            count3 = count3 + 1

    def test_e(self):
        '''数据库更新竞价金额为0.01'''
        count4 = 0
        while count4 < 3:
            sql3 = "update fhb_order_pay_management set money = '0.01' where fhb_order_id = '" + orderid[count4] + "'"
            print(sql3)
            cursor3 = global_var.db.cursor()
            # 执行SQL语句
            cursor3.execute(sql3)
            # MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
            global_var.db.commit()
            time.sleep(1)
            count4 = count4 + 1
        time.sleep(1)

    def test_f(self):
        '''发起审批'''
        global_var.db.connect()
        sql5 = "select id from fhb_order_pay_management where fhb_order_id = '" + orderid1 + "'"
        cursor5 = global_var.db.cursor()
        cursor5.execute(sql5)
        results5 = cursor5.fetchall()
        # 有多个的情况，取第一个订单的id
        spid1 = results5[0]['id']
        print("第一个审批id:" + spid1)

        global_var.db.connect()
        sql6 = "select id from fhb_order_pay_management where fhb_order_id = '" + orderid2 + "'"
        cursor6 = global_var.db.cursor()
        cursor6.execute(sql6)
        results6 = cursor6.fetchall()
        # 有多个的情况，取第一个订单的id
        spid2 = results6[0]['id']
        print("第二个审批id:" + spid2)

        global_var.db.connect()
        sql7 = "select id from fhb_order_pay_management where fhb_order_id = '" + orderid3 + "'"
        cursor7 = global_var.db.cursor()
        cursor7.execute(sql7)
        results7 = cursor7.fetchall()
        # 有多个的情况，取第一个订单的id
        spid3 = results7[0]['id']
        print("第三个审批id:" + spid3)
        url5 = "http://" + global_var.api_host + "/ms-fahuobao-order/pay-management/sponsor-audit"
        data5 = [
            {
                "id": spid1,
                "money": 0.01
            },
            {
                "id": spid2,
                "money": 0.01
            },
            {
                "id": spid3,
                "money": 0.01
            }
        ]
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=global_var.headers1)
        print("发起审批:" + request5.text)
        time.sleep(5)
        self.assertIn(global_var.arg1, request5.text, msg='测试fail')

    def test_g(self):
        '''标记审批通过'''
        global_var.db.connect()
        sql8 = "select package_id from fhb_order_pay_package_item where order_no = '" + orderno1 + "'"
        print(sql8)
        cursor8 = global_var.db.cursor()
        cursor8.execute(sql8)
        results8 = cursor8.fetchall()
        global pageId
        pageId = results8[0]['package_id']
        print("支付包id:" + pageId)

        global_var.db.connect()
        sql9 = "select id from fhb_order_pay_package_item where order_no = '" + orderno1 + "'"
        cursor9 = global_var.db.cursor()
        cursor9.execute(sql9)
        results9 = cursor9.fetchall()
        packageItemId1 = results9[0]['id']
        print("第一个支付单id:" + packageItemId1)

        global_var.db.connect()
        sql10 = "select id from fhb_order_pay_package_item where order_no = '" + orderno2 + "'"
        cursor10 = global_var.db.cursor()
        cursor10.execute(sql10)
        results10 = cursor10.fetchall()
        packageItemId2 = results10[0]['id']
        print("第二个支付单id:" + packageItemId2)

        sql11 = "select id from fhb_order_pay_package_item where order_no = '" + orderno3 + "'"
        cursor11 = global_var.db.cursor()
        cursor11.execute(sql11)
        results11 = cursor11.fetchall()
        packageItemId3 = results11[0]['id']
        print("第三个支付单id:" + packageItemId3)

        url8 = "http://" + global_var.api_host + "/ms-fahuobao-order/pay-management/update-tab"
        data8 = {
            "pageId": pageId,
            "tabStatus": "P-250",
            "packageItemIdList": [
                packageItemId1,
                packageItemId2,
                packageItemId3
            ]
        }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=global_var.headers1)
        print("标记审批通过:" + request8.text)
        time.sleep(2)
        self.assertIn(global_var.arg1, request8.text, msg='测试fail')

    def test_h(self):
        '''提交审批结果'''
        url9 = "http://" + global_var.api_host + "/ms-fahuobao-order/payPackage/modifyPackageStatus"
        data9 = {"packageId": pageId, "tabState": 1}
        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=global_var.headers1)
        print("提交审批结果:" + request9.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request9.text, msg='测试fail')

    def test_i(self):
        '''钱包余额支付'''
        url10 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/balance-pay-pay-management"
        data10 = {"pageId": pageId, "money": 0.03, "password": "123456"}
        request10 = requests.request("POST", url=url10, data=json.dumps(data10), headers=global_var.headers1)
        print("钱包余额支付:" + request10.text)
        self.assertIn(global_var.arg1, request10.text, msg='测试fail')

if __name__ == "__main__":
    unittest.main()