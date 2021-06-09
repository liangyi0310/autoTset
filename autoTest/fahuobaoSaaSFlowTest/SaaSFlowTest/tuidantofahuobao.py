import unittest
import requests
import json
import datetime
import time
#导入公用参数readConfig.py
from Common.readConfig import *

class TestMethod(unittest.TestCase):    # 定义一个类，继承自unittest.TestCase
    '''配装正常流程测试'''
    def test_a(self):
        url_scm = "http://192.168.10.59:3000/api/ms-user-info/user/userLogin"
        data_scm = {"loginName":"liangyi","pwd":"123456"}
        head = {'Content-Type':'application/json'}
        res = requests.post(url=url_scm,data=json.dumps(data_scm),headers = head)
        token_scm = res.json()['data']['token']
        print(token_scm)
        global header2
        header2 = {
            'Content-Type': 'application/json',
            'token': token_scm
        }

    def test_b(self):
        '''录单'''
        #录单接口
        url1 = "http://192.168.10.59:3000/api/ms-order-data/orderData/insertData"
        i = datetime.datetime.now()
        print("收件人姓名：家具配装测试" + str(i.month) + str(i.day))
        consignee_name1 = "推单平台" + str(i.month) + str(i.day) + str(i.minute) + str(i.second)
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
                "serviceNo": "SETE04",
                "orderSource": "",
                "verifyServiceNo": "",
                "collectionMoney": 0,
                "consigneeAddress": "1",
                "isElevator": "1",
                "consigneeName": consignee_name1,
                "floor": "",
                "consigneePhone": "15023621702",
                "province": "四川省",
                "provinceNo": "510000",
                "city": "成都市",
                "cityNo": "510100",
                "district": "双流区",
                "districtNo": "510116",
                "street": "东升街道",
                "streetNo": "510116001",
                "trunkId": "",
                "trunkName": "",
                "trunkOrderNo": "",
                "branch": "成都市网点DLCK",
                "branchId": "2bc5829c-41e3-11e7-97d1-0242ac120021",
                "lineNo": "",
                "trunkDestinationNo": "510100",
                "branchMemo": "",
                "orderTrunkArriveInfo": {
                    "memo": "",
                    "provinceNo": "510000",
                    "cityNo": "510100",
                    "districtNo": "510116"
                },
                "transportType": "YSFS02",
                "dot": {
                    "name": "成都市网点DLCK",
                    "trunkDestination": "成都市",
                    "id": "2bc5829c-41e3-11e7-97d1-0242ac120021",
                    "trunkDestinationNo": "510100"
                },
                "totalVolume": "1",
                "totalWeight": "1",
                "cargoPrice": "1",
                "totalBalse": "",
                "orderGoodss": [
                    {
                        "name": "折叠床/午休床（电动）",
                        "installFee": "",
                        "num": "1",
                        "balse": "1",
                        "goodsNo": "J021001"
                    }
                ],
                "isLightHeavy": "1",
                "orderCosts": [
                {
                        "costNo": "FLTE02",
                        "suggestFee": "暂无",
                        "recountMoney": "0.01",
                        "memo": ""
                },
                {
                        "costNo": "FLTE03",
                        "suggestFee": "暂无",
                        "recountMoney": "0.01",
                        "memo": ""
                },
                {
                        "costNo": "FLTE04",
                        "suggestFee": 0,
                        "recountMoney": "0.01",
                        "memo": ""
                }
            ],
                "supportValue": "",
                "isTemp": "false",
                "handleType": 1
        }
        request1 = requests.post( url1, data = json.dumps(data1) ,headers = header2)
        print("录单：" + request1.text)
        time.sleep(3)
        self.assertIn(global_var.arg1, request1.text, msg='测试fail')

if __name__ == "__main__":
    unittest.main()