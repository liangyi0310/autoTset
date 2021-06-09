# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import datetime
import time


# 发货宝web端操作用户18883612485
headers1 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'SJZ',
            'tokenSecret' : '123456',
            'systemCode':'FAHUOBAO'
}

# app端操作用户,平台师傅秦敏18599937985
headers2 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'XRQM',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
}

# 运营后台web端操作用户,scm用户18883612485
headers3 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'YYHTQM',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
}

# 需要测试的环境
api_host = "192.168.10.56:8763"

Pictureid = '5b4ef81bd423d40001f0195e'
# 录单使用的产品信息
goods =    [
        {
            "num":1,
            "picture":Pictureid,
            "memo":"",
            "bigClassNo":"FHB02",
            "middleClassNo":"FHB02008",
            "pictureType":2,
            "pictureName":"2018012214"
        }
    ]
def addorder():

    #发货宝录单接口
    url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"

    i = datetime.datetime.now()
    print("收件人姓名：退款流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute))

    data1 =        {
            "businessNo": "BSTE02",
            "serviceNo": "FHB02",
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
            "isArriva": 2,
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

def connectdb():

    # 打开数据库连接
    db = pymysql.connect(host='192.168.10.59', port=3307, user='fahuobao', password='jjt.123', db='fahuobao',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    return db

def tuikuanflow(db):

    i = datetime.datetime.now()
    consignee_name1 = "退款流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)

    # 通过订单的收件人姓名查询出订单id
    sql1 = "SELECT fhb_order_id FROM fhb_order_consignee_info WHERE consigne_name = '"+consignee_name1+"' ORDER BY foundtime DESC"

    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        orderid = results[0]["fhb_order_id"]
        # orderno = results[0]['order_no']
        print("订单id:" + orderid)
        # print("订单编号:" + orderno)

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

        # 通过师傅id查询竞价记录
        db.connect()
        # sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
        sql2 = "SELECT id,fhb_order_id FROM fhb_order_bidding_log WHERE fhb_order_id= '" + orderid + "' ORDER BY foundtime DESC"
        # 使用cursor()方法获取操作游标
        cursor2 = db.cursor()
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results2 = cursor2.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        fhb_order_id='%s' %(orderid)
        
        jingjiaid = results2[0]['id']
        print("订单id:" + fhb_order_id)
        print("竞价id:" + jingjiaid)

        # 修改竞价金额为0.01
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()

        # 选择师傅接口
        url3="http://" +  api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?orderId="+fhb_order_id+"&biddingLogId="+jingjiaid+""
        request_tuikuan = requests.request("GET", url=url3, headers=headers1)
        # tuikuan_data = json.loads(request_tuikuan.text)
        # result3 = tuikuan_data['data']
        # print(result3)
        # data3 = result3[0]
        # XZpeople=data3['people']
        # print("选择师傅"+XZpeople)

        # 支付接口，objectList为订单id
        url4 = "http://" +  api_host + "/ms-user-wallet/wallet/balance-pay"
        data4 = {"objectList":[fhb_order_id],"money":0.01,"password":"123456"}
        # print(data4)
        # print(json.dumps(data4))
        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("支付：" + request4.text)

        # 发起退款
        # url5 = "http://" +  api_host + "/ms-fahuobao-order/merRefund/saveOrderRefundRecord"
        # data5 = {"refundAmount": "0.01", "refundMemo": "", "refundPic": "", "refundOrderState": 1, "orderId": fhb_order_id}
        # # print(data5)
        # # print(json.dumps(data5))
        # time.sleep(2)
        # request5 = requests.request("POST", url=url5, data=json.dumps(data5), headers=headers1)
        # print("发起退款：" + request5.text)
        #
        # # 师傅不同意转仲裁
        # url6 = "http://" +  api_host + "/ms-fahuobao-order/merRefund/saveAuditOrderRefundRecord"
        # data6 = {
        #     "memo":"951",
        #     "state":1,
        #     "picture":[
        #         "5b4ef81bd423d40001f0195e"
        #     ],
        #     "orderId":fhb_order_id
        # }
        #
        # request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=headers2)
        # print("不同意转仲裁：" + request6.text)
        # #
        # # 仲裁处理
        # url7 = "http://" +  api_host + "/ms-fahuobao-order/merRefund/saveArbitrateOrderRefundRecord"
        # data7 = {
        #         "arbitrateAmount":"0.01",
        #         "arbitratePic":"5b4ef81bd423d40001f0195e",
        #         "arbitrateMemo":"32132",
        #         "orderId":fhb_order_id
        #     }
        # request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers3)
        # print("仲裁处理：" + request7.text)

    except:
        print("Error: unable to fecth data")

def closedb(db):
    # 关闭数据库连接
    db.close()

def main():
    addorder()
    db = connectdb()
    tuikuanflow(db)
    closedb(db)



if __name__ == '__main__':
    main()