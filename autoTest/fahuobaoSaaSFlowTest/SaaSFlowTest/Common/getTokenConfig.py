'''获取各个登录账号token'''
import requests
import json

class global_one:
    api_host = "192.168.10.59:3102"
    api_host1 = "192.168.10.59:8763"
    headers_null = {'Content-Type': 'application/json'}
    url_login = "http://" + api_host + "/api/ms-common-user/user/login"
    url_login1 = "http://" + api_host1 + "/ms-common-user/user/login"

    '''发货宝web登录：15023621999'''
    data_login_fhb = {"phone": "15023621999", "pwd": "123456", "projectType": "fhbMant"}
    request_login_fhb = requests.request("POST", url=url_login, data=json.dumps(data_login_fhb), headers=headers_null)
    response = request_login_fhb.json()
    '''获取josn数据中的键值'''
    fhb_token = response['data']['token']

    '''app登录：15023621791 成都地区'''
    # 合并app登录 15023621791
    data_login_app = {"equipmentId": "355757010445621", "phone": "15023621791", "projectType": "platWorker","pushClientId": "7a78305e75c6989d4c97a2c8baecee36", "verifyCode": "896522"}
    request_login_app = requests.request("POST", url=url_login1, data=json.dumps(data_login_app), headers=headers_null)
    response2 = request_login_app.json()
    app_token = response2['data']['token']

    '''运营后台登录：18599937985'''
    data_login_admin = {"phone": "18599937985", "pwd": "123456", "projectType": "fhbBack"}
    request_login_admin = requests.request("POST", url=url_login, data=json.dumps(data_login_admin),headers=headers_null)
    response3 = request_login_admin.json()
    admin_token = response3['data']['token']

    '''直营登录：18599937985'''
    data_login_storeWeb = {"loginName": "18599937985", "pwd": "123456", "phone": "18599937985","projectType": "storeWeb"}
    request_login_storeWeb = requests.request("POST", url=url_login1, data=json.dumps(data_login_storeWeb),headers=headers_null)
    response4 = request_login_storeWeb.json()
    storeWeb_token = response4['data']['token']

def set_value(fhb_token,app_token,admin_token,storeWeb_token):
    global_one.storeWeb_token = storeWeb_token
    global_one.admin_token = admin_token
    global_one.fhb_token = app_token
    global_one.fhb_token = fhb_token

def get_value():
    return global_one.fhb_token,global_one.app_token,global_one.admin_token,global_one.storeWeb_token


