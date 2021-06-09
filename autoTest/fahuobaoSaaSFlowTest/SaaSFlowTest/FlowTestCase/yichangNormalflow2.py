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
            'tokenCode' : 'QM',
            'tokenSecret' : '123456',
            'systemCode':'SCM',
}
headers1={'Content-Type' : 'application/json',
          "Accept":"*/*",
"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyLXR5cGUiOm51bGwsInVzZXItbmFtZSI6Iua1i-ivlei0puiuoeWIkiIsInVzZXItcGFyYW0iOiJ7XCJ1c2VyUGhvbmVcIjpcIjE4ODgzNjEyNDg1XCIsXCJpc0FkbWluXCI6MX0iLCJ1c2VyLXN1YmplY3Rpb24iOiI1YTJhMjEwNC0wZjcwLTQ0YjctOWEwZS1jOTU2N2M1ZDFkYjAiLCJ1c2VyLWlkIjoiNWEyYTIxMDQtMGY3MC00NGI3LTlhMGUtYzk1NjdjNWQxZGIwIiwiaXNzIjoiMTg4ODM2MTI0ODUiLCJ1c2VyLWNvZGUiOiIxODg4MzYxMjQ4NSIsImV4cCI6MTUzNjE1MzM1NiwiaWF0IjoxNTM2MTM4OTU2fQ.rplQqyyFbT5-9SoDTIQTwMADI1RZcCtVJF2v9LWNSLk"
        }

headers2={'Content-Type' : 'application/json',
            "Accept":"*/*",
"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyLXR5cGUiOiJEWExYMDUiLCJ1c2VyLW5hbWUiOiJ2aGNodnUiLCJ1c2VyLXBhcmFtIjoie1widXNlclBob25lXCI6XCIxODU5OTkzNzk4NVwiLFwiaXNBZG1pblwiOjEsXCJoZWFkUGhvdG9cIjpcIjViODc1N2U1NWIxZmFjMDAwMTk3NGY0NFwifSIsInVzZXItc3ViamVjdGlvbiI6IjBjYWNjNjU4LWRkMjktNDBiYi05YzY5LWIyZTE5Njc3Mjc1ZiIsInVzZXItaWQiOiIwY2FjYzY1OC1kZDI5LTQwYmItOWM2OS1iMmUxOTY3NzI3NWYiLCJpc3MiOiJVSUQyNTA4MDAyNTA4IiwidXNlci1jb2RlIjoiVUlEMjUwODAwMjUwOCIsImV4cCI6MTUzODYyNDc2MSwiaWF0IjoxNTM2MDMyNzYxfQ.vaajjKhUcHhS9opu380wuBssvSTfT5ZmjyA-0E74NHs"
          }

# 需要测试的环境
api_host = "192.168.10.56:8763"

# 录单使用的产品信息
goods = [
            {
                "num": 1,
                "picture": "J080103",
                "memo": "产品说明:",
                "bigClassNo": "J08",
                "middleClassNo": "J080103",
                "pictureType": "1"
            }
        ]

def addorder():

    #发货宝录单接口
    url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"

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

def connectdb():
    # 打开数据库连接
    db = pymysql.connect(host='192.168.10.59', port=3307, user='fahuobao', password='jjt.123', db='fahuobao',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    db2 = pymysql.connect(host='192.168.10.70', port=3306, user='mydbz', password='qazwsx..', db='athena',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return db,db2



def yichangflow(db,db2):

    i = datetime.datetime.now()
    consigne_name1 = "异常流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)

    # 通过订单的收件人姓名查询出订单id
    sql1 = "SELECT fhb_order_id,order_no FROM fhb_order_consignee_info a inner join  fhb_order b on a.fhb_order_id=b.id WHERE a.consigne_name = '"+consigne_name1+"' ORDER BY a.foundtime DESC"

    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
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

        # 通过师傅id查询竞价记录
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
        fhb_order_id=orderid
        jingjiaid = results2[0]['id']
        print("订单id:" + fhb_order_id)
        print("竞价id:" + jingjiaid)
        # db.close()

        # 修改竞价金额为0.01
        sql3 = "UPDATE fhb_order_bidding_log set money = '0.01' where fhb_order_id = '" + orderid + "'"
        print(sql3)
        cursor3 = db.cursor()
        # 执行SQL语句
        cursor3.execute(sql3)
        #MySQL的默认存储引擎就是InnoDB， 所以对数据库数据的操作会在事先分配的缓存中进行， 只有在commit之后， 数据库的数据才会改变
        db.commit()

        # 选择接口
        url3 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/choice-pay?t=1531964865851&orderId="+fhb_order_id+"&biddingLogId="+jingjiaid+""
        request_yichang = requests.request("GET", url=url3, headers=headers1)
        # tuikuan_data = json.loads(request_tuikuan.text)
        # result3 = tuikuan_data['data']
        # print(result3)
        # data3 = result3[0]
        # XZpeople=data3['people']
        # print("选择师傅"+XZpeople)

        # data3 = result1[0]
        # request3 = requests.request("GET", url=url3, data=json.dumps(data3), headers=headers1)
        # print("选择师傅：" + request3.text)

        # 支付接口，objectList为订单id
        time.sleep(5)
        url4 = "http://" +  api_host + "/ms-user-wallet/wallet/balance-pay"
        data4 = {"objectList":[fhb_order_id],"money":0.01,"password":"123456"}

        request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
        print("支付：" + request4.text)

        # 通过发货宝订单编号查出scm订单id与订单编号

        time.sleep(10)
        db2.connect()
        sql4 = "select id,order_no from order_data where order_no='"+orderno+"'"

        # 使用cursor()方法获取操作游标
        cursor3 = db2.cursor()
        # 执行SQL语句
        cursor3.execute(sql4)
        # 获取所有记录列表
        results3 = cursor3.fetchall()
        # print(results[0])
        # 有多个的情况，取第一个订单的id
        scmorderid = results3[0]['id']
        scmorderno=results[0]['order_no']
        print("scm订单id:" + scmorderid)
        print("scm订单编号:" + scmorderno)

        # db2.close()

        # 预约
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

        # 师傅发起异常
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

        # 通过订单id查出异常id
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
        yichangid = results5[0]['id']
        print("异常id:" + yichangid)

        # 货主给出方案
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

        # # 师傅不同意货主方案（发起仲裁）
        # url7 = "http://" +  api_host + "/ms-fahuobao-order-abnormal/FhbOrderAbnormal/workerApplyArbitration"
        # data7 = {
        #             "pic":[
        #                 Pictureid
        #             ],
        #             "schemeDesc":"321",
        #             "id":yichangid
        #         }
        # request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers2)
        # print("师傅不同意货主方案（发起仲裁）：" + request7.text)
        #
        # # 仲裁处理
        # url7 = "http://" + api_host + "/ms-fahuobao-order-abnormal/FhbOrderAbnormal/dealArbitration"
        # data7 ={"schemeDesc":"321321","pic":[Pictureid],"id":yichangid}
        # request7 = requests.request("POST", url=url7, data=json.dumps(data7), headers=headers3)
        # print("仲裁处理：" + request7.text)
    except:
        print("Error: unable to fecth data")

def closedb(db,db2):
    # 关闭数据库连接1:59
    db.close()
    db2.close()



def main():
    addorder()
    db,db2 = connectdb()
    yichangflow(db,db2)
    closedb(db,db2)

if __name__ == '__main__':
    main()
