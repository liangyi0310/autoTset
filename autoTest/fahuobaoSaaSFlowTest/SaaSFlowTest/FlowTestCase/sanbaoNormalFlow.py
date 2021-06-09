# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import datetime

# web端操作用户
headers1 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'D',
            'tokenSecret' : '123456',
            'systemCode':'SCM'
}

# app端操作用户,小段网点负责人13558630480
headers2 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'XD',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
}

# 需要测试的环境
api_host = "192.168.10.56:8763"

# 录单使用的产品信息
goods = [{
                "name": "推拉(趟门)衣柜:2m＜长度≤2.5m",
                "installFee": 440,
                "num": "2",
                "balse": "3",
                "goodsNo": "J010208"
            }, {
                "name": "家用吧台(带附柜)",
                "installFee": 120,
                "num": "1",
                "balse": "2",
                "goodsNo": "J040502"
            }]

def addorder():

    #网点分拣接口：
    url_branch_sorting="http://" +  api_host + "/ms-sorting/trunkSortingController/branchSorting?provinceNo=430000&cityNo=430100&districtNo=430103&streetNo=430103002&serviceNo=SETE01&merchantId=8a095966-421b-11e7-b3cd-0050569f7b0c"

    request_trunk = requests.request("GET", url=url_branch_sorting, headers=headers1)
    branch_data = json.loads(request_trunk.text)
    result1 = branch_data['data']
    data1 = result1[0]
    branchname= data1['branch']
    branchid= data1['branchId']

    #线路分拣接口：
    url_trunk_sorting="http://" +  api_host + "/ms-sorting/trunkSortingController/trunkSorting?serviceNo=SETE01&provinceNo=430000&cityNo=430100&districtNo=430103&orderId="
    request_trunk = requests.request("GET", url=url_trunk_sorting, headers=headers1)
    trunk_data = json.loads(request_trunk.text)
    result1 = trunk_data['data']
    data1 = result1[0]
    lineno= data1['lineNo']
    trunkid= data1['trunkId']
    trunkname = data1['trunkName']

    #录单接口
    url1 = "http://" +  api_host + "/ms-order-data/orderData/insertData"

    i = datetime.datetime.now()
    print("收件人姓名：三包测试" + str(i.month) + str(i.day))

    data1 = {
            "merchantId": "8a095966-421b-11e7-b3cd-0050569f7b0c",
            "merchant": "奥琦家具",
            "merchantOrder": "",
            "clearingSubject": "2bd8b24f-421e-11e7-b3cd-0050569f7b0c",
            "clearingSubjectId": "2bd8b24f-421e-11e7-b3cd-0050569f7b0c",
            "cleaningType": "",
            "cleaningCycle": "",
            "clearingTypeNo": "ZQ",
            "clearingTypeName": "周期",
            "payLogistics": "",
            "tempMerchantBean": {
                "name": "",
                "clearingModeNo": "",
                "payModeNo": "",
                "id": ""
            },
            "clearingModeNo": "",
            "payTypeNo": "",
            "orderSign": "",
            "clearingCycleName": "十天",
            "boolCollection": "0",
            "businessNo": "BSTE02",
            "serviceNo": "SETE01",
            "orderSource": "",
            "verifyServiceNo": "",
            "collectionMoney": 0,
            "consigneeAddress": "213213123",
            "isElevator": "1",
            "consigneeName": "三包测试" + str(i.month) + str(i.day),
            "floor": "22",
            "consigneePhone": "17608017801",
            "province": "湖南省",
            "provinceNo": "430000",
            "city": "长沙市",
            "cityNo": "430100",
            "district": "天心区",
            "districtNo": "430103",
            "street": "坡子街街道",
            "streetNo": "430103002",
            "trunkId": trunkid,
            "trunkName": trunkname,
            "trunkOrderNo": "2131231313",
            "branch": branchname,
            "branchId": branchid,
            "lineNo": lineno,
            "trunkDestinationNo": "430100",
            "branchMemo": "网点备注网点备注网点备注网点备注",
            "orderTrunkArriveInfo": {
                "memo": "物流备注物流备注物流备注",
                "provinceNo": "430000",
                "cityNo": "430100",
                "districtNo": "430103"
            },
            "transportType": "YSFS02",
            "getSortingId": "7ca63c45-4c73-11e8-9e5d-0242ac130002",
            "dot": {
                "name": "长沙市网点DCSX",
                "trunkDestination": "长沙市",
                "id": "2bc12dae-41e3-11e7-97d1-0242ac120021",
                "trunkDestinationNo": "430100"
            },
            "totalVolume": "6",
            "totalWeight": "4",
            "cargoPrice": "8888",
            "totalBalse": "",
            "orderGoodss": goods,
            "isLightHeavy": "1",
            "orderCosts": [{
                "costNo": "FLTE01",
                "suggestFee": 660,
                "recountMoney": "660",
                "memo": ""
            }, {
                "costNo": "FLTE02",
                "suggestFee": 440,
                "recountMoney": "440",
                "memo": ""
            }, {
                "costNo": "FLTE03",
                "suggestFee": 560,
                "recountMoney": "560",
                "memo": ""
            }, {
                "costNo": "FLTE04",
                "suggestFee": 0,
                "recountMoney": "0",
                "memo": ""
            }, {
                "costNo": "FLTE05",
                "suggestFee": "暂无",
                "recountMoney": "10",
                "memo": ""
            }],
            "supportValue": "5000",
            "isTemp": "false",
            "handleType": 1
        }

    request1 = requests.request("POST", url=url1, data = json.dumps(data1) ,headers = headers1)

    print("录单：" + request1.text)

def connectdb():

    # 打开数据库连接
    db = pymysql.connect(host='192.168.10.70', port=3306, user='mydbz', password='qazwsx..', db='athena',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    return db

def normalflow(db):

    i = datetime.datetime.now()
    consignee_name1 = "三包测试" + str(i.month) + str(i.day)

    # 通过订单的收件人姓名查询出订单id
    sql1 = "SELECT id,order_no FROM order_data WHERE consignee_name = '" + consignee_name1 + "' ORDER BY foundtime DESC"

    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        orderid = results[0]['id']
        orderno = results[0]['order_no']
        print("订单id:" + orderid)
        print("订单编号:" + orderno)

        db.close()

        # 末端转单接口，将订单转到小段网点，负责人13558630480
        url2 = "http://" +  api_host + "/ms-order-turn/turn/modifyBranchs"
        data2 = {
            "modifyType": "1",
            "turnMoney": "",
            "branchId": "ad4c9ec3-338f-432d-a04c-de95abee261a",
            "saleId": "",
            "orderIds": [orderid]
        }

        request2 = requests.request("POST", url=url2, data=json.dumps(data2), headers=headers1)
        print("末端转单：" + request2.text)

        # 入库接口
        url3 = "http://" +  api_host + "/ms-order-data/putInStorage/putInStorage"
        data3 = {"id": orderid}

        request3 = requests.request("POST", url=url3, data=json.dumps(data3), headers=headers1)
        print("入库：" + request3.text)

        # 出库接口
        url4 = "http://" +  api_host + "/ms-order-data/outBound/outBound"
        data4 = [{"orderNo": orderno, "id": orderid, "trunkOrderNo": "",
                  "trunkObj": {"value": "b96b0f77-420c-11e7-b3cd-0050569f7b0c", "text": "佛山市顺德区天喜物流有限公司"},
                  "trunkId": "b96b0f77-420c-11e7-b3cd-0050569f7b0c", "trunkName": "佛山市顺德区天喜物流有限公司"}]

        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("出库：" + request4.text)

        # 到件接口
        url5 = "http://" +  api_host + "/ms-order-data/arrive/arrive"
        data5 = {
                 "deliveryContacts": "测试",
                 "deliveryPhone": "213213213",
                 "contactsAddress": [{
                  "text": "湖南省",
                  "value": "430000"
                 }, {
                  "text": "长沙市",
                  "value": "430100"
                 }, {
                  "text": "开福区",
                  "value": "430105"
                 }],
                 "deliveryAddress": "测试",
                 "deliveryMemo": "测试",
                 "id": orderid,
                 "provinceNo": "430000",
                 "cityNo": "430100",
                 "districtNo": "430105"
                }

        request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers1)
        print("到件：" + request5.text)

        # 预约接口-预约派单一体
        url6 = "http://" +  api_host + "/ms-order-data/appOrder/appointappoint-distributionOne-choose"
        data6 = {"branchUserId":"04bd7638-57eb-11e7-aa39-0242ac120004","cause":"车辆送不过来","codeYT":"night","ids":[orderid],"timeYT":str(i.year) + "-" + str(i.month) + "-" + str(i.day)}

        request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=headers2)
        print("预约：" + request6.text)

        # 提货接口

        db.connect()
        sql2 = "select id from assign_worker where order_id= '" + orderid + "'"
        cursor2 = db.cursor()
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # print(results2[0])
        assignid = results2[0]["id"]

        url7 = "http://" +  api_host + "/ms-order-data/appOrder/pickGoods"
        data7 = {"assignId":assignid,"serviceTypeCode":"CZSETE01"}

        request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers2)
        print("提货：" + request7.text)

        # 上门接口
        url8 = "http://" + api_host + "/ms-order-data/appOrder/houseCall?assignId=" + assignid + "&orderId=" + orderid

        request8 = requests.request("POST", url=url8, headers=headers2)
        print("上门：" + request8.text)

        # 签收接口
        url9 = "http://" + api_host + "/ms-order-data/appOrder/appOrderSign"
        data9 = {"accuracy":5.0,"assignId":assignid,"comment":"","imgId":["5ae2c5046f5e5d00015fec8c"],"jdVerificationCode":"","quality":5.0,"serviceTypeCode":"CZSETE01","signimgid":["5ae2c5046f5e5d00015fec8c"],"solid":5.0}

        request9 = requests.request("POST", url=url9, data=json.dumps(data9), headers=headers2)
        print("签收：" + request9.text)

    except:
        print("Error: unable to fecth data")

def closedb(db):
    # 关闭数据库连接
    db.close()

def main():
    addorder()
    db = connectdb()
    normalflow(db)
    closedb(db)


if __name__ == '__main__':
    main()
