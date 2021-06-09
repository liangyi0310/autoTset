from Common.getTokenConfig import *
import pymysql
class global_var:
    '''需要定义全局变量的放在这里，最好定义一个初始值'''
    '''发货宝web登录：15023621999'''
    headers1 = {
        'Content-Type': 'application/json',
        'token': global_one.fhb_token
    }
    '''app登录：15023621791 成都地区'''
    headers2 = {
        'Content-Type': 'application/json',
        'token': global_one.app_token
    }
    '''运营后台登录：18599937985'''
    headers3 = {
        'Content-Type': 'application/json',
        'token': global_one.admin_token
    }
    '''直营登录：18599937985'''
    headers4 = {
        'Content-Type': 'application/json',
        'token': global_one.storeWeb_token
    }
    #产品配置信息
    Pictureid = '5c12261f818563000163c507'  # 图片id
    goods = [
                {
                    "num": "1",
                    "pictureType": 2,
                    "picture": "5c12261f818563000163c507",
                    "bigClassNo": "FHB02",
                    "middleClassNo": "FHB02010",
                    "pictureName": "产品名称HH",
                    "goodsId": "6c90c34d-7d89-4d65-a969-46da3214e2e1"
                }
            ]
    arg1 = '"success":true'
    api_host = "192.168.10.59:3102"
    #服务类型
    '''配送安装'''
    serviceNo_PZ = "FHB02,FHB03"
    db_fahuobao = pymysql.connect(host="192.168.10.59", port=3307, user="fahuobao", password="jjt.123", db="fahuobao",
                             charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    db_common = pymysql.connect(host="192.168.10.59", port=3307, user="fahuobao", password="jjt.123", db="common",
                         charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    db_storage = pymysql.connect(host="192.168.10.59", port=3307, user="fahuobao", password="jjt.123", db="storage",
                                charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    db_athena = pymysql.connect(host='192.168.10.70', port=3306, user='develop', password='qazwsx123', db='athena',
                              charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    db_commonuser = pymysql.connect(host='192.168.10.70', port=3306, user='develop', password='qazwsx123', db='commonuser',
                              charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    db_workflow = pymysql.connect(host='192.168.10.70', port=3306, user='develop', password='qazwsx123', db='workflow',
                              charset='utf8', cursorclass=pymysql.cursors.DictCursor)

# 对于每个全局变量，都需要定义get_value和set_value接口
def set_value(headers1,headers2,headers3,headers4,goods,api_host,arg1,db_fahuobao,db_common,db_storage,db_athena,db_commonuser,db_workflow,serviceNo_PZ):
    global_var.headers1 = headers1
    global_var.headers2 = headers2
    global_var.headers3 = headers3
    global_var.headers4 = headers4
    global_var.api_host = api_host
    global_var.goods = goods
    global_var.arg1 = arg1
    global_var.db_fahuobao = db_fahuobao
    global_var.db_common = db_common
    global_var.db_storage = db_storage
    global_var.db_athena = db_athena
    global_var.db_commonuser = db_commonuser
    global_var.db_workflow = db_workflow
    global_var.db_workflow = serviceNo_PZ

def get_value():
    return global_var.headers1,global_var.headers2,global_var.headers3,global_var.headers4,global_var.goods,global_var.api_host,global_var.arg1,global_var.db_fahuobao,global_var.db_common,global_var.db_storage,global_var.db_athena,global_var.db_commonuser,global_var.db_workflow,global_var.serviceNo_PZ

def closedb(db_fahuobao,db_common,db_storage,db_athena,db_commonuser,db_workflow):
    # 关闭数据库连接
    db_fahuobao.close()
    db_common.close()
    db_storage.close()
    db_athena.close()
    db_commonuser.close()
    db_workflow.close()