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
    def test_a(self):
        '''录单'''
        url1 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"
        i = datetime.datetime.now()
        print("收件人姓名：再次下单流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))

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
                "consigneeName": "再次下单流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute),
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
        # 打开数据库连接 ,db为59数据库,db1为70数据库
        '''通过订单的收件人姓名查询出订单id、订单编号'''
        global i
        i = datetime.datetime.now()
        consignee_name1 = "再次下单流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)

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
        # db.connect()
        '''修改竞价金额为0.01'''
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
        '''发起退款-关闭原单'''
        url5 = "http://" +  api_host + "/ms-fahuobao-order/merRefund/saveOrderRefundRecord"
        #refundOrderState=1：不关闭原单，=2：关闭原单
        data5 = {"refundAmount": "0.01", "refundMemo": "", "refundPic": "", "refundOrderState": 2, "orderId": fhb_order_id}
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
        self.assertIn(global_var.arg1, request7.text, msg='测试filed')

    def test_k(self):
        #查询发货宝订单状态
        '''查询发货宝订单状态'''
        # 使用cursor()方法获取操作游标
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

    def test_l(self):
        # 再次下单
        '''再次下单'''
        url8 = "http://" + global_var.api_host + "/ms-fahuobao-order/FhbOrderAgain/saveOrderAgain"
        data8 = {
                "orderId":orderid
        }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=headers1)
        print("再次下单：" + request8.text)
        self.assertIn(global_var.arg1, request8.text, msg='测试filed')

    def test_m(self):
        # print('竞价')
        # 将订单推到天心区并用185这个账号进行竞价
        '''将订单推到天心区并用185这个账号进行竞价'''
        url9 = "http://" + api_host + "/ms-fahuobao-order/bidding/quoted-price"
        data9 = {
            "memo": "",
            "money": "200",
            "orderId": orderid
        }

        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=headers2)
        print("竞价：" + request9.text)
        time.sleep(2)
        self.assertIn(arg1, request9.text, msg='测试faild')

    def test_n(self):
        # 通过师傅id查询竞价记录
        '''通过师傅id查询竞价记录'''
        global_var.db.connect()
        sql5 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '" + orderid + "' ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor5 = global_var.db.cursor()
        # 执行SQL语句
        cursor5.execute(sql5)
        # 获取所有记录列表
        results5 = cursor5.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global fhb_order_id, jingjiaid
        fhb_order_id = orderid
        jingjiaid = results5[0]['id']
        print("订单id:" + fhb_order_id)
        print("竞价id:" + jingjiaid)
        # db.close()
        time.sleep(2)

    def test_o(self):
        # 修改竞价金额为0.01
        '''修改竞价金额为0.01'''
        # db.connect()
        sql6 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql6)
        cursor6 = db.cursor()
        # 执行SQL语句
        cursor6.execute(sql6)
        # MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()

    def test_p(self):
        # 选择师傅接口
        '''选择师傅'''
        url10 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId=" + fhb_order_id + "&biddingLogId=" + jingjiaid + ""
        request10 = requests.request("GET", url=url10, headers=headers1)
        time.sleep(2)
        self.assertIn(arg1, request10.text, msg='测试filed')

    def test_q(self):
        # 支付接口，objectList为订单id
        '''支付'''
        time.sleep(5)
        url11 = "http://" + global_var.api_host + "/ms-fahuobao-user/wallet/balance-pay"
        data11 = {"objectList": [fhb_order_id], "money": 0.01, "password": "123456"}
        # print(data4)
        # print(json.dumps(data4))
        request11 = requests.request("POST", url=url11, data=json.dumps(data11), headers=headers1)
        print("支付：" + request11.text)
        time.sleep(2)
        self.assertIn(arg1, request11.text, msg='测试filed')

    def test_r(self):
        # 通过发货宝订单编号查出scm订单id与订单编号
        '''通过发货宝订单编号查出scm订单id与订单编号'''
        time.sleep(5)
        db1.connect()
        sql7 = "select id,order_no from order_data where order_no='" + orderno + "'"

        # 使用cursor()方法获取操作游标
        cursor7 = db1.cursor()
        # 执行SQL语句
        cursor7.execute(sql7)
        # 获取所有记录列表
        results7 = cursor7.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        global scmorderid, scmorderno
        scmorderid = results7[0]['id']
        scmorderno = results7[0]['order_no']
        print("scm订单id:" + scmorderid)
        print("scm订单编号:" + scmorderno)

        # db2.close()

    def test_s(self):
        # 预约
        '''预约'''
        url12 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/appointappoint-distributionOne-choose"
        data12 = {
            "branchUserId": "",
            "cause": "",
            "codeYT": "night",
            "ids": [scmorderid],
            "timeYT": str(i.year) + "-" + str(i.month) + "-" + str(i.day)
        }
        # print(json.dumps(data5))
        request12 = requests.request("POST", url=url12, data=json.dumps(data12), headers=headers2)
        print("预约：" + request12.text)
        time.sleep(2)
        self.assertIn(arg1, request12.text, msg='测试field')

    def test_t(self):
        '''查询assignid'''
        db1.connect()
        sql8 = "select id from assign_worker where order_id = '" + scmorderid + "'"
        print(sql8)
        cursor8 = db1.cursor()
        cursor8.execute(sql8)
        # 获取所有记录列表
        results8 = cursor8.fetchall()
        # print(results6[0])
        global assignid
        assignid = results8[0]["id"]
        print("assigned:" + assignid)

    def test_u(self):
        '''提货'''
        url13 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/pickGoods"
        data13 = {"assignId": assignid, "imgId": ["5b5810b5d423d400017bf0c2"], "serviceTypeCode": "CZSETE01"}
        request13 = requests.request("POST", url=url13, data=json.dumps(data13), headers=headers2)
        print("提货：" + request13.text)
        time.sleep(3)
        self.assertIn(arg1, request13.text, msg='测试field')

    def test_v(self):
        '''上门'''
        # 上门
        url14 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/houseCall?assignId=" + assignid + "&orderId=" + assignid + ""  # post请求拼接
        request14 = requests.request("POST", url=url14, headers=headers2)
        print("上门：" + request14.text)
        time.sleep(2)
        self.assertIn(arg1, request14.text, msg='测试field')

    def test_w(self):
        '''查询出订单服务码'''
        db.connect()
        sql9 = "select service_code from fhb_order where order_no = '" + orderno + "'"
        print(sql9)
        cursor9 = db.cursor()
        cursor9.execute(sql9)
        # 获取所有记录列表
        results9 = cursor9.fetchall()
        # print(results6[0])
        global service_code
        service_code = results9[0]["service_code"]
        time.sleep(3)
        print(service_code)

    def test_x(self):
        '''签收'''
        url15 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/appOrderSign"
        data15 = {
            "assignId": assignid,
            "imgId": ["5b581a07d423d400017bf0d2"],
            "jdVerificationCode": "",
            "qmImg": "5b581a00d423d400017bf0d0",
            "serviceCode": service_code,
            "serviceTypeCode": "CZSETE01"
        }
        request15 = requests.request("POST", url=url15, data=json.dumps(data15), headers=headers2)
        print("签收：" + request15.text)
        time.sleep(2)
        self.assertIn(arg1, request15.text, msg='测试field')

    def test_y(self):
        # 发货宝商家评价
        '''发货宝商家评价'''
        url16 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/evaluation"
        data16 = {"fhbOrderId": fhb_order_id, "stars": 5, "pictures": "", "memo": "", "tips": ""}
        time.sleep(2)
        request16 = requests.request("POST", url=url16, data=json.dumps(data16), headers=headers1)
        print("发货宝商家评价：" + request16.text)
        time.sleep(2)
        self.assertIn(arg1, request16.text, msg='测试field')

    def test_z(self):
        # 使用cursor()方法获取操作游标
        '''查询订单所有费用之和'''
        db.connect()
        time.sleep(2)
        cursor10 = db.cursor()
        # 查询订单所有费用之和
        sql10 = "select sum(money) from fhb_order_cost where order_id='" + orderid + "'order by found_date desc limit 10"
        # 执行SQL语句
        cursor10.execute(sql10)
        time.sleep(3)
        # 获取所有记录列表
        results10 = cursor10.fetchall()
        # print(results7)
        summoney = results10[0]['sum(money)']
        # 断言结果正确时，返回的结果是None,错误时则会抛错
        if self.assertEqual(summoney, 0.00) == None:
            print('订单所有费用之和：' + str(summoney), "订单费用结算正确")
        else:
            time.sleep(2)
            cursor11 = db.cursor()
            # 查询订单费用信息
            sql11 = "select cost_name,money from fhb_order_cost where order_id='" + orderid + "'order by found_date desc limit 10"
            # 执行SQL语句
            cursor11.execute(sql11)
            time.sleep(3)
            # 获取所有记录列表
            results11 = cursor11.fetchall()
            cost_name_list = []
            for cost_all in results11:
                cost_name_list.append(cost_all)
            print("订单费用清单明细:" + str(cost_name_list))

    def test_za(self):
        # 订单结算
        '''订单结算'''
        url17 = "http://" + api_host + "/ms-fahuobao-order-data/order-wallet/clearing-confirm?t=1536315925677"
        data17 = scmorderid
        print(json.dumps(data17))
        time.sleep(2)
        # post请求传参不是json格式时，不需要转换为json，否则会报错
        request17 = requests.request("POST", url=url17, data=data17, headers=headers1)
        print("发货宝商家评价：" + request17.text)
        time.sleep(2)
        self.assertIn(arg1, request17.text, msg='测试field')

    def test_zb(self):
        # 使用cursor()方法获取操作游标
        '''查询师傅钱包流水'''
        db.connect()
        time.sleep(2)
        cursor12 = db.cursor()
        # 师傅钱包流水
        sql12 = "select money,trading_object_name,fee_name from wallet_bill_running_log where out_no='" + scmorderno + "'"
        # 执行SQL语句
        cursor12.execute(sql12)
        time.sleep(3)
        # 获取所有记录列表
        results12 = cursor12.fetchall()
        # print(results7)
        money = results12[0]['money']
        worker_name = results12[0]['trading_object_name']
        moneyname = results12[0]['fee_name']
        print('订单收入金额为%2.2f,收入对象为%s,费用名称为%s' % (money, worker_name, moneyname))


if __name__ == '__main__':
    unittest.main()