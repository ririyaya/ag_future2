import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
from decimal import Decimal
from decimal import getcontext
import traceback

table_name='ag30'

mydb = mysql.connector.connect(
host="localhost",
    user="root",
    passwd="111",
    database='koudai',  # 数据库
    auth_plugin= 'mysql_native_password',unix_socket='/private/tmp/mysql.sock') # 'caching_sha2_password')#
d = mydb.cursor()

                 # type1, 2, 3,  4,  5:
def get(count, tm,table_name):  #1m,5m,15m,30m,60m qid: 6 agtd, 13 xag, 704 连续
    if table_name=='ag15':
        url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=3&count=" + str(count) + "&ts=" + str(tm)
    else:url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=4&count=" + str(count) + "&ts=" + str(tm)
    header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
    r = requests.post(url, headers=header)
    candle = json.loads(r.text)['data']['candle']
    li = []
    for i in range(0, len(candle)):
        li.append(tuple(candle[i].values()))
    #print(len(li))
    ts = li[0][7]  # 倒叙最新
    return li, ts


re_sq='select t from (select count(ts)t,ts from '+table_name+' group by ts)b where t>1'
del_sq='delete from '+table_name+' order by ts desc limit 1'
get_sq = 'select ts from '+table_name+' order by ts desc limit 1'
d.execute(del_sq)
d.execute(get_sq)
lasttime = int((d.fetchall())[0][0])
#lasttime=1533566880000-1

sq = 'insert into '+table_name+' (a,c,t,v,h,l,o,ts) values(%s,%s,%s,%s,%s,%s,%s,%s)'
count = 114
flag = 0
li = []
tm = int(time.time() * 1000)

for i in range(0,666):
    print(i)
    # tm=1620111600000+i*1000*60*60*count
    if tm <= 1533566880000-1:
        break
    rev = get(count, tm,table_name)
    print(rev[0][-1][-1],lasttime)
    #rev[0].reverse()
    for i in range(len(rev[0])):
        #print(i, rev[0][i][2])
        if rev[0][i][7] == lasttime:
            rev = (rev[0][i + 1:], rev[1])
            flag=1
            break
    li, tm = rev[0] + li, rev[1]
    time.sleep(1)
    if flag==1:
        break

print(len(li))
d.executemany(sq,li)

mydb.commit()
time.sleep(1)
'''
print('new table name')
t_name=str(input())
ctable_sq='create table '+ t_name +' as (select * from temp group by ts,a,h,l,c,o,t)'
truncate_sq='truncate temp'

try:
    d.execute(ctable_sq)
    d.execute(truncate_sq)
    mydb.commit()
except:
    traceback.print_exc()'''