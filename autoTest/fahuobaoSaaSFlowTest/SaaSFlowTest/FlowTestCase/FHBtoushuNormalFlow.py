# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import datetime
import time
from Common.newReadConfig import *


# 发货宝web端操作用户18883612485
headers1 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'QM',
            'tokenSecret' : '123456',
            'systemCode':'FAHUOBAO'
}

# app端操作用户,平台师傅秦敏18599937985
headers2 = {
            'Content-Type' : 'application/json',
            'tokenCode' : 'XRLY2',
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

# 微信小程序用户,无需token
headers4 = {
            'Content-Type' : 'application/json',
}
# 需要测试的环境
api_host = "192.168.10.56:8763"


# headers1={'Content-Type' : 'application/json',
# "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyLXR5cGUiOm51bGwsInVzZXItbmFtZSI6Iua1i-ivlei0puiuoeWIkiIsInVzZXItcGFyYW0iOiJ7XCJ1c2VyUGhvbmVcIjpcIjE4ODgzNjEyNDg1XCIsXCJpc0FkbWluXCI6MX0iLCJ1c2VyLXN1YmplY3Rpb24iOiI1YTJhMjEwNC0wZjcwLTQ0YjctOWEwZS1jOTU2N2M1ZDFkYjAiLCJ1c2VyLWlkIjoiNWEyYTIxMDQtMGY3MC00NGI3LTlhMGUtYzk1NjdjNWQxZGIwIiwiaXNzIjoiMTg4ODM2MTI0ODUiLCJ1c2VyLWNvZGUiOiIxODg4MzYxMjQ4NSIsImV4cCI6MTUzNjIzMzA1OCwiaWF0IjoxNTM2MjE4NjU4fQ.nvK3rWY7O-aoObltDEqjGuN50h9V6wxdwGZMBFsqvHQ"
#         }
#
# headers2={'Content-Type' : 'application/json',
# "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyLXR5cGUiOiJEWExYMDUiLCJ1c2VyLW5hbWUiOiLmooHmr4UiLCJ1c2VyLXBhcmFtIjoie1widXNlclBob25lXCI6XCIxNTAyMzYyMTcwMlwiLFwiaXNBZG1pblwiOjEsXCJoZWFkUGhvdG9cIjpcIjViN2ZhNWZkNWIxZmFjMDAwMTNiNTYyMVwifSIsInVzZXItc3ViamVjdGlvbiI6IjMzYjkyZThjLTZkMzgtNGI4MS05NGRlLTRlOGNjNjU2ODcxOCIsInVzZXItaWQiOiIzM2I5MmU4Yy02ZDM4LTRiODEtOTRkZS00ZThjYzY1Njg3MTgiLCJpc3MiOiJVSUQ1MDM4MDA1MDM4IiwidXNlci1jb2RlIjoiVUlENTAzODAwNTAzOCIsImV4cCI6MTUzODgwODg0OSwiaWF0IjoxNTM2MjE2ODQ5fQ.Zc4L0mv-eR--cYakGfPIYF6RGGFnNyNq9HlCI_NskKs"
#           }
#图片id
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
for a in range(10):
    def addorder():

        #发货宝录单接口
        url1 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/saveOrder"

        i = datetime.datetime.now()
        print("收件人姓名：商家投诉流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+':'+str(i.minute))

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
                "consigneeName": "商家投诉流程测试"+ str(i.month) + str(i.day)+'-'+str(i.hour)+':'+str(i.minute),
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
        db2 = pymysql.connect(host='192.168.10.70', port=3306, user='mydbz', password='qazwsx..', db='athena',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        return db,db2


    def tousuflow(db,db2):

        i = datetime.datetime.now()
        consigne_name1 = "商家投诉流程测试" + str(i.month) + str(i.day)+'-'+str(i.hour)+':'+str(i.minute)

        # 通过订单的收件人姓名查询出订单id
        db.connect()
        time.sleep(2)
        sql1 = "SELECT fhb_order_id,order_no,service_code FROM fhb_order_consignee_info a inner join  fhb_order b on a.fhb_order_id=b.id WHERE a.consigne_name = '"+consigne_name1+"' ORDER BY a.foundtime DESC"

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
            orderno=results[0]['order_no']
            # service_code=results[0]['service_code']
            print("订单id:" + orderid)
            print("订单编号:" + orderno)
            # print("服务码:" + service_code)


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
            # sql2 = "SELECT id,fhb_order_id,people_user_id FROM fhb_order_bidding_log WHERE people_user_id ='0cacc658-dd29-40bb-9c69-b2e19677275f' and fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
            sql2="SELECT id,fhb_order_id,people_user_id FROM fhb_order_bidding_log WHERE  fhb_order_id= '"+orderid+"' ORDER BY foundtime DESC"
            print(sql2)
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
            jingjiashifuid=results2[0]['people_user_id']
            print("订单id:" + fhb_order_id)
            print("竞价id:" + jingjiaid)
            print("竞价师傅id:" + jingjiashifuid)

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

            url4 = "http://" +  api_host + "/ms-user-wallet/wallet/balance-pay"
            data4 = {"objectList":[fhb_order_id],"money":0.01,"password":"123456"}

            request4 = requests.request("POST", url=url4, data=json.dumps(data4), headers=headers1)
            print("支付：" + request4.text)
            # 通过发货宝订单编号查出scm订单id与订单编号
            time.sleep(5)
            db2.connect()
            sql4 = "select id,order_no from order_data where order_no='"+orderno+"'"

            # 使用cursor()方法获取操作游标
            cursor4 = db2.cursor()
            # 执行SQL语句
            cursor4.execute(sql4)
            # 获取所有记录列表
            results4 = cursor4.fetchall()
            # print(results[0])
            # 有多个的情况，取第一个订单的id
            scmorderid = results4[0]['id']
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

            # 提货
            db2.connect()
            sql5 = "select id from assign_worker where order_id = '" + scmorderid + "'"
            print(sql5)
            cursor5 = db2.cursor()
            cursor5.execute(sql5)
            # 获取所有记录列表
            results5 = cursor5.fetchall()
            # print(results6[0])
            assignid = results5[0]["id"]
            print("assigned:"+assignid)
            url6 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/pickGoods"
            data6 = {"assignId":assignid,"imgId":["5b5810b5d423d400017bf0c2"],"serviceTypeCode":"CZSETE01"}
            request6 = requests.request("POST", url=url6, data=json.dumps(data6), headers=headers2)
            print("提货：" + request6.text)
            time.sleep(3)


            # 上门
            url7 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/houseCall?assignId=" + assignid + "&orderId=" + assignid +"" #post请求拼接
            request7 = requests.request("POST", url=url7, headers=headers2)
            print("上门：" + request7.text)


            # 签收
            db.connect()
            sql6 = "select service_code from fhb_order where order_no = '" + orderno + "'"
            print(sql6)
            cursor6 = db.cursor()
            cursor6.execute(sql6)
            # 获取所有记录列表
            results6 = cursor6.fetchall()
            # print(results6[0])
            service_code = results6[0]["service_code"]
            time.sleep(3)
            print(service_code)
            url8 = "http://" + api_host + "/ms-fahuobao-order-data/appOrder/appOrderSign"
            data8 = {
                        "assignId": assignid,
                        "imgId": ["5b581a07d423d400017bf0d2"],
                        "jdVerificationCode": "",
                        "qmImg": "5b581a00d423d400017bf0d0",
                        "serviceCode": service_code,
                        "serviceTypeCode": "CZSETE01"
                    }
            request8 = requests.request("POST", url=url8, data=json.dumps(data8), headers=headers2)
            print("签收：" + request8.text)
            # 客户发起投诉
            print("师傅id:"+jingjiashifuid)

            Pictureid='5b4ef81bd423d40001f0195e'
            # 发货宝商家评价
            # url9 = "http://" +  api_host + "/ms-fahuobao-order/FhbOrder/evaluation"
            # data9 = {"fhbOrderId":fhb_order_id,"stars":5,"pictures":"","memo":"","tips":""}
            # print(json.dumps(data9))
            # time.sleep(2)
            # request9 = requests.request("POST", url=url9, data=json.dumps(data9),headers = headers1)
            # print("发货宝商家评价：" + request9.text)
        #
        #     # # 发货宝商家发起投诉
        #     # url10 = "http://" +  api_host + "/ms-fahuobao-order/merchantComplain/complain"
        #     # data10 ={"complainCauseCode":"CAUSE1","complainMemo":"231","complainPicture":[Pictureid],"fhbOrderId":fhb_order_id}
        #     #
        #     # request9 = requests.request("POST", url=url10, data=json.dumps(data10),headers = headers1)
        #     # print("发货宝商家发起投诉：" + request6.text)
        #     #
        #     # # 投诉处理
        #     # time.sleep(5)
        #     # db.connect()
        #     # sql7 = "select id from fhb_complain_record where order_id='"+fhb_order_id+"' and worker_id='"+jingjiashifuid+"' order by foundtime desc"
        #     #
        #     # # 使用cursor()方法获取操作游标
        #     # cursor7 = db.cursor()
        #     # # 执行SQL语句
        #     # cursor7.execute(sql7)
        #     # # 获取所有记录列表
        #     # results7 = cursor7.fetchall()
        #     # # print(results[0])
        #     # # 有多个的情况，取第一个订单的id
        #     # tousuid = results7[0]['id']
        #     # print("投诉id:" + tousuid)
        #
        #     # # 投诉处理
        #     # url11 = "http://" +  api_host + "/ms-fahuobao-order/fhbComplain/complainRecordBean"
        #     # data11 = {"dealImg":[],"boolReal":1,"dealWithNo":"COMPLAINRESULT3","dealWithDeduct":"","dealWithMemo":"32231231","complainId":tousuid}
        #     # request11 = requests.request("POST", url=url11, data=json.dumps(data11), headers=headers3)
        #     # print("投诉处理：" + request7.text)
        #
        except:
            print("Error: unable to fecth data")

def closedb(db,db2):
    # 关闭数据库连接
    db.close()
    db2.close()



def main():
    addorder()
    db,db2 = connectdb()
    tousuflow(db,db2)
    closedb(db,db2)

if __name__ == '__main__':
    main()
