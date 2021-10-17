import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
import talib
from decimal import Decimal
from decimal import getcontext

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="111",
    database='koudai',  # 数据库
    auth_plugin='mysql_native_password')  # 'caching_sha2_password')
d = mydb.cursor()


def get(count, tm):  # type1,2,3,4,5:1m,5m,15m,30m,60m qid 6,agtd,13 xag
    url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=6&type=4&count=" + str(
        count) + "&ts=" + str(tm)
    header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
    r = requests.post(url, headers=header)
    candle = json.loads(r.text)['data']['candle']
    li = []
    for i in range(0, len(candle)):
        li.append(tuple(candle[i].values()))
    ts = li[0][7]  # 倒叙最新
    return li, ts


get_sq = "select ts from agtd order by ts desc limit 1"
d.execute(get_sq)
lasttime = (d.fetchall())[0][0]

sq = "insert into agtd(a,c,t,v,h,l,o,ts) values(%s,%s,%s,%s,%s,%s,%s,%s)"
count = 129
flag = 0
li = []
tm = int(time.time() * 1000)

for i in range(0,2):
    print(i)
    # tm=1620111600000+i*1000*60*60*count
    if tm <= 1534951140001:
        break
    rev = get(count, tm)
    print(rev[0][-1][-1],lasttime)
    #rev[0].reverse()
    for i in range(len(rev[0])):
        #print(i, rev[0][i][2])
        if rev[0][i][7] >= lasttime:
            rev = (rev[0][i + 1:], rev[1])
            flag=1
            break
    li, tm = rev[0] + li, rev[1]
    time.sleep(0.50)
    if flag==1:
        break

# li.reverse()
#print(li)
d.executemany(sq, li)
mydb.commit()
