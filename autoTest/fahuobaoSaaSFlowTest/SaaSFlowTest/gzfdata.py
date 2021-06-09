import requests
import time
from openpyxl import Workbook

def getOnePage(page):
    header={'Content-Type':'application/x-www-form-urlencoded', 'Referer':'http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/applicationresultdetail/24'}
    # data={'isInit':'true', 'pageNumber':str(page), 'tableName':'QUERY25'}
    url='http://www.cqgzfglj.gov.cn:9090/site/cqgzf/queryresultpublic/getSqshjgAction'
    page='?isInit=true&pageNumber='+str(page)+'&prefix=&xm=&cnumber=&sqpq=&code=&tableName=QUERY25'
    resp=requests.post(url=url+page, headers=header, timeout=10)
    return resp

if __name__ == "__main__":
    wb = Workbook()
    ws = wb.active
    for a in range(2034):
        r=getOnePage(a+1)
        if r.status_code != 200:
            continue
        gzf=r.json()['dataList']
        print(a+1)
        for i in range(50):
            c = []
            for v in gzf[i-1].values():
                c.append(v)
            ws.append(c)
        # time.sleep(1)
    wb.save(r'd://gzfdata.xlsx')