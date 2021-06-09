import requests
import xlwt
import xlrd
from lxml import etree
import requests
import pymysql
import json
import datetime
import time
arg1 = "两室一厅"
arg2 = "大竹林"
arg3 = "鸳鸯"
arg4 = "华岩"
arg5 = "茶园"
arg6 = "龙州湾"
arg7 = "井口-美丽阳光家园"
arg8 = "南岸区-江南水岸"
arg9 = "蔡家"
arg10 = "钓鱼嘴-半岛逸景●乐园"
arg11 = "碚都佳园"
arg12 = "龙洲南苑"
arg13 = "西永"
arg14 = "木耳"
arg15 = "界石"
arg16 = "陈家桥-学府悦园"
arg17 = "缙云新居"
headers1 = {
            'Referer' : 'http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/applicationresultdetail/24'
}


class gongZuData(object):

    def __init__(self):
        self.f = xlwt.Workbook()  #创建工作薄
        self.sheet1 = self.f.add_sheet(u'图书列表',cell_overwrite_ok=True)#命名table
        self.rowsTitle = [u'申请编号',u'姓名',u'性别',u'工作单位',u'个人收入',u'家庭收入',u'申请方式',u'有无住房',u'住房面积',u'申请片区',u'状态',u'申请时间','申请户型']#创建标题
        for i in range(0, len(self.rowsTitle)):
            #最后一个参数设置样式
            self.sheet1.write(0, i, self.rowsTitle[i], self.set_style('Times new Roman', 220, True))
        #Excel保存位置
        self.f.save('C:/Users/Administrator/Desktop/gongzu.xlsx')
    #该函数设置字体样式
    def set_style(self,name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.colour_index = 2
        font.height = height
        style.font = font
        return style

    # def getUrl(self):
    #     for i in range(10):
    #         url = 'https://book.douban.com/top250?start={}'.format(i*25)
    #         self.spiderPage(url)

    def gongzu(self):
        count = 1
        while (count < 3):
            request1 = requests.request("POST",
                                        url="http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/getSqshjgAction"
                                            "?isInit=true&prefix=&pageNumber=" + str(
                                            count) + "&xm=&cnumber=&sqpq=&code=&tableName=QUERY25", headers=headers1)
            # print(request1.url)
            print("第" + str(count) + "页:" + request1.text)
            # i = 0
            # self.assertIn(arg1, request1.text, msg = "no")
            time.sleep(1)
            count = count + 1

    def spiderPage(self,url):
        if url is None:
           return None

        try:
           data = xlrd.open_workbook('C:/Users/Administrator/Desktop/gongzu.xlsx')#打开Excel文件
           table = data.sheets()[0] #通过索引顺序获取table，因为初始化时只创建了一个table，因此索引值为0
           rowCount = table.nrows  #获取行数   ，下次从这一行开始
           proxies = {#使用代理IP，获取IP的方式在上一篇文章爬虫打卡4中有叙述
            'http':'http://110.73.1.47:8123'}
           user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
           headers = {'User-Agent': user_agent}
           respon=requests.get(url, headers=headers,proxies=proxies)#获得响应
           htmlText=respon.text#打印html内容
           s = etree.HTML(htmlText)#将源码转化为能被XPath匹配的格式
           trs = s.xpath('//*[@id="content"]/div/div[1]/div/table/tr')#提取相同的前缀
           m = 0
           for tr in trs:
               data = []
               bookHref=tr.xpath('./td[2]/div[1]/a/@href')
               bookTitle=tr.xpath('./td[2]/div[1]/a/text()')
               bookScore=tr.xpath('./td[2]/div[2]/span[2]/text()')
               bookPeople=tr.xpath('./td[2]/div[2]/span[3]/text()')
               bookImg=tr.xpath('./td[1]/a/img/@src')
               bookHref = bookHref[0] if bookHref else ''    # python的三目运算 :为真时的结果 if 判定条件 else 为假时的结果
               bookTitle = bookTitle[0] if bookTitle else ''
               bookScore = bookScore[0] if bookScore else ''
               bookPeople =bookPeople[0] if bookPeople else ''
               bookImg = bookImg[0] if bookImg else ''

            #拼装成一个列表
               data.append(rowCount+m)  #为每条书添加序号
               data.append(bookHref)
               data.append(bookTitle)
               data.append(bookScore)
               data.append(bookPeople)
               data.append(bookImg)

               for i in range(len(data)):
                   self.sheet1.write(rowCount+m,i,data[i]) #写入数据到execl中

               m+=1   #记录行数增量
               print(m)
               print (bookHref,bookTitle,bookScore,bookPeople,bookImg)

        except Exception as e:
               print ('出错',type(e),e)

        finally:
            self.f.save('C:/Users/Administrator/Desktop/gongzu.xlsx')


if '_main_':
    dbBook = gongZuData()
    dbBook.gongzu()