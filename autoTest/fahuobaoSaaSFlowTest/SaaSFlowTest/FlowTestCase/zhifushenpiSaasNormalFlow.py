# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import datetime
import time

# web端操作用户
headers1 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'LY',
            'tokenSecret' : '123456',
            'systemCode':'FAHUOBAO'
}

# app端操作用户,小段网点负责人13558630480
headers2 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'XRLY',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
}
headers3 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'LYSCM',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
            'X-Requested-With': 'XMLHttpRequest',
}
# 需要测试的环境
api_host = "192.168.10.56:8763"

# 录单使用的产品信息
goods = [
            {
                "num": 1,
                "picture": "J020800",
                "memo": "产品描述XX",
                "bigClassNo": "J02",
                "middleClassNo": "J020800",
                "pictureType": "1"
            }
        ]


def addorder():
    print("\033[0;35;m-------------------------------------------------------------------居家智享支付审批流程运行开始-------------------------------------------------------------------\033[0m")

    print("\033[0;32;m**************************************************录单**************************************************\033[0m")
    #录单接口
    url1 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"

    i = datetime.datetime.now()
    print("收件人姓名：yi支付审批" + str(i.month) + str(i.day) + str(i.second) + str(i.microsecond))

    data1 = {
                "businessNo": "BSTE02",
                "serviceNo": "FHB01",
                "orderWay": "1",
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
                "memo": "备注:\n",
                "isArriva": 1,
                "boolCollection": "0",
                "collectionMoney": "",
                "collectionMemo": "",
                "allVolume": "3",
                "allWeight": "12",
                "allPackages": "4",
                "allCargoPrice": "245",
                "consigneeName": "yi支付审批" + str(i.month) + str(i.day) + str(i.second) + str(i.microsecond),
                "consigneePhone": "15023621702",
                "consigneeAddress": "详细地址",
                "floor": "12",
                "deliveryName": "提货联系:支装测试",
                "deliveryPhone": "15023621702",
                "deliveryMemo": "提货备注:",
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

    count=0
    while (count < 3):
        request1 = requests.request("POST", url=url1, data = json.dumps(data1) ,headers = headers1)
        print("录单：" + request1.text)
        time.sleep(2)
        count = count +1


def connectdb():

    # 打开数据库连接
    db = pymysql.connect(host="192.168.10.59", port=3307, user="fahuobao", password="jjt.123", db="fahuobao",
                         charset="utf8", cursorclass=pymysql.cursors.DictCursor)

    db1 = pymysql.connect(host='192.168.10.70', port=3306, user='mydbz', password='qazwsx..', db='athena',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    return db,db1

def normalflow(db,db1):
    i = datetime.datetime.now()
    consignee_name1 = "yi支付审批" + str(i.month) + str(i.day)

    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 通过订单的收件人姓名查询出订单id
        sql1 = "select id,order_no from fhb_order where id in (select fhb_order_id from fhb_order_consignee_info where consigne_name like '%" + consignee_name1 + "%') ORDER BY foundtime DESC"
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        orderid1 = results[0]['id']
        orderid2 = results[1]['id']
        orderid3 = results[2]['id']
        orderno1 = results[0]['order_no']
        orderno2 = results[1]['order_no']
        orderno3 = results[2]['order_no']

        print("第一个订单id:" + orderid1 + "第二个订单id:" + orderid2 + "第三个订单id:" + orderid3)
        print("第一个订单编号:" + orderno1 + "第二个订单编号:" + orderno2 + "第三个订单编号:" + orderno3)


        # 师傅报价
        print("\033[0;32;m**************************************************师傅报价**************************************************\033[0m")
        url2 = "http://" + api_host + "/ms-fahuobao-order/bidding/quoted-price"
        count1 = 0
        orderid = [orderid1,orderid2,orderid3]
        while count1 < 3:
            data2 = {
            "memo": "",
            "money": "200",
            "orderId": orderid[count1]
            }
            request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers2)
            print("师傅报价：" + request2.text)
            time.sleep(1)
            count1 = count1 + 1
        # web端报价中选择师傅
        print("\033[0;32;m**************************************************web端报价中选择师傅**************************************************\033[0m")
        db.connect()
        sql2 = "select id from fhb_order_bidding_log where fhb_order_id in (select fhb_order_id from fhb_order_consignee_info where consigne_name like '%" + consignee_name1 + "%') ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = db.cursor()
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

        biddinglogid = [biddinglogid1,biddinglogid2,biddinglogid3]
        while count3 < 3:
            url3 = "http://" + api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId=" + orderid[count3] + "&biddingLogId=" + biddinglogid[count3] + ""
            request3 = requests.get(url3, headers=headers1)
            print("选择师傅：" + request3.text)
            time.sleep(1)
            count3 = count3 + 1

        print("\033[0;32;m*********************************数据库更新支付金额为0.01*********************************\033[0m")
        # 数据库更新竞价金额为0.01
        count4 = 0

        while count4 < 3:
            sql3 = "update fhb_order_pay_management set money = '0.01' where fhb_order_id = '" + orderid[count4] + "'"
            print(sql3)
            cursor3 = db.cursor()
            # 执行SQL语句
            cursor3.execute(sql3)
            #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
            db.commit()
            time.sleep(1)
            count4 = count4 + 1

        time.sleep(1)

        print("\033[0;32;m**************************************************发起审批**************************************************\033[0m")
        db.connect()
        sql5 = "select id from fhb_order_pay_management where fhb_order_id = '"+ orderid1 + "'"
        cursor5 = db.cursor()
        cursor5.execute(sql5)
        results5 = cursor5.fetchall()
        # 有多个的情况，取第一个订单的id
        spid1 = results5[0]['id']
        print("第一个审批id:" + spid1)

        db.connect()
        sql6 = "select id from fhb_order_pay_management where fhb_order_id = '" + orderid2 + "'"
        cursor6 = db.cursor()
        cursor6.execute(sql6)
        results6 = cursor6.fetchall()
        # 有多个的情况，取第一个订单的id
        spid2 = results6[0]['id']
        print("第二个审批id:" + spid2)

        db.connect()
        sql7 = "select id from fhb_order_pay_management where fhb_order_id = '" + orderid3 + "'"
        cursor7 = db.cursor()
        cursor7.execute(sql7)
        results7 = cursor7.fetchall()
        # 有多个的情况，取第一个订单的id
        spid3 = results7[0]['id']
        print("第三个审批id:" + spid3)

        url5 = "http://" + api_host + "/ms-fahuobao-order/pay-management/sponsor-audit"
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
        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers1)
        print("发起审批:" + request5.text)

        time.sleep(5)

        print("\033[0;32;m**************************************************标记审批通过**************************************************\033[0m")

        db.connect()
        sql8 = "select package_id from fhb_order_pay_package_item where order_no = '" + orderno1 + "'"
        print(sql8)
        cursor8 = db.cursor()
        cursor8.execute(sql8)
        results8 = cursor8.fetchall()
        pageId = results8[0]['package_id']
        print("支付包id:" + pageId)

        db.connect()
        sql9 = "select id from fhb_order_pay_package_item where order_no = '" + orderno1 + "'"
        cursor9 = db.cursor()
        cursor9.execute(sql9)
        results9 = cursor9.fetchall()
        packageItemId1 = results9[0]['id']
        print("第一个支付单id:" + packageItemId1)

        db.connect()
        sql10 = "select id from fhb_order_pay_package_item where order_no = '" + orderno2 + "'"
        cursor10 = db.cursor()
        cursor10.execute(sql10)
        results10 = cursor10.fetchall()
        packageItemId2 = results10[0]['id']
        print("第二个支付单id:" + packageItemId2)

        sql11 = "select id from fhb_order_pay_package_item where order_no = '" + orderno3 + "'"
        cursor11 = db.cursor()
        cursor11.execute(sql11)
        results11 = cursor11.fetchall()
        packageItemId3 = results11[0]['id']
        print("第三个支付单id:" + packageItemId3)

        url8 = "http://" + api_host + "/ms-fahuobao-order/pay-management/update-tab"
        data8 = {
                    "pageId": pageId,
                    "tabStatus": "P-250",
                    "packageItemIdList": [
                        packageItemId1,
                        packageItemId2,
                        packageItemId3
                    ]
                }
        request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=headers1)
        print("标记审批通过:" + request8.text)

        time.sleep(2)

        print("\033[0;32;m**************************************************提交审批结果**************************************************\033[0m")
        url9 =  "http://" + api_host + "/ms-fahuobao-order/payPackage/modifyPackageStatus"
        data9 = {"packageId":pageId,"tabState":1}
        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=headers1)
        print("提交审批结果:" + request9.text)

        time.sleep(3)

        print("\033[0;32;m**************************************************钱包余额支付**************************************************\033[0m")
        url10 = "http://" + api_host + "/ms-fahuobao-user/wallet/balance-pay-pay-management"
        data10 = {"pageId":pageId,"money":0.03,"password":"123456"}
        request10 = requests.request("POST", url=url10, data=json.dumps(data10), headers=headers1)
        print("钱包余额支付:" + request10.text)

        print("\033[0;35;m-------------------------------------------------------------------居家智享支付审批流程测试结束-------------------------------------------------------------------\033[0m")

    except:
        print("Error: unable to fecth data")

def closedb(db,db1):
    # 关闭数据库连接
    db.close()
    db1.close()

def main():
    addorder()
    db,db1 = connectdb()
    normalflow(db,db1)
    closedb(db,db1)


if __name__ == '__main__':
    main()
