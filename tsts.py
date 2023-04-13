import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
# import talib
from decimal import Decimal
from decimal import getcontext
import traceback
#load data local infile "/Users/v_yangxing04/Downloads/ugc16.csv" into table ugc16 fields terminated by ','  enclosed by '"' lines terminated by '\n' ignore 1 rows;


class CONNECTSQL(object):

    def __init__(self,table_name,type,count=114):
        re_sq = 'select t from (select count(ts)t,ts from ' + table_name + ' group by ts)b where t>1'
        del_sq = 'delete from ' + table_name + ' order by ts desc limit 1'
        get_sq = 'select ts from ' + table_name + ' order by ts desc limit 1'
        self.updata_sq = 'insert into ' + table_name + ' (a,c,t,v,h,l,o,ts) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        self.mydb = mysql.connector.connect(
        host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            buffered=True,
            auth_plugin= 'mysql_native_password',unix_socket='/private/tmp/mysql.sock'
        ) # 'caching_sha2_password')#
        self.d = self.mydb.cursor()
        self.d.execute(del_sq)
        self.d.execute(get_sq)
        self.lasttime = 1333566880000 - 1
        # self.lasttime = int((self.d.fetchall())[0][0])
        self.type=type
        self.count = count

     # type1, 2, 3,  4,  5:
    def get(self,count, tm):  # 1m,5m,15m,30m,60m     8:1d                    qid: 6 agtd,  13 xag, 704 ag连续
        url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=" + str(
            self.type) + "&count=" + str(count) + "&ts=" + str(tm)
        header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
        r = requests.post(url, headers=header)
        candle = json.loads(r.text)['data']['candle']
        li = []
        for i in range(0, len(candle)):
            li.append(tuple(candle[i].values()))
        #print(len(li))
        ts = li[0][7]  # 倒叙最新
        return li, ts

    def updatedb(self,mydb):
        li = []
        flag = 0
        tm = int(time.time() * 1000)
        try:
            for i in range(0, 30):
                print(i)
                # tm=1620111600000+i*1000*60*60*count
                if tm <= 1533566880000 - 1:
                    break
                rev = self.get(self.count, tm)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(rev[0][-1][-1] / 1000)),
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lasttime / 1000)))
                # rev[0].reverse()
                for i in range(len(rev[0])):
                    # print(i, rev[0][i][2])
                    if rev[0][i][7] == self.lasttime:
                        rev = (rev[0][i + 1:], rev[1])
                        flag = 1
                        break
                li, tm = rev[0] + li, rev[1]
                if flag == 1:
                    break
                time.sleep(1)

        except:
            print(len(li))
            self.d.executemany(self.updata_sq, li)
            mydb.commit()
            print('error')
            time.sleep(1)

        print(len(li))
        self.d.executemany(self.updata_sq, li)
        mydb.commit()
        time.sleep(1)

    def updatetxt(self):
        #if os.path.exists(r"d:\databuffer.txt"):
            #os.remove(r"d:\databuffer.txt")
        li = []
        flag = 0
        tm = int(time.time() * 1000)
        tm=1557764520000
        with open(r"d:\databuffer.txt", "a", encoding='utf-8') as f:
            try:
                for i in range(0, 400):
                    print(i)
                    # tm=1620111600000+i*1000*60*60*count
                    if tm <= 1533566880000 - 1:
                        break
                    rev = self.get(self.count, tm)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(rev[0][-1][-1] / 1000)), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lasttime/ 1000)))
                    # rev[0].reverse()
                    for i in range(len(rev[0])):
                        # print(i, rev[0][i][2])
                        if rev[0][i][7] == self.lasttime:
                            rev = (rev[0][i + 1:], rev[1])
                            flag = 1
                            break
                    li, tm = rev[0] + li, rev[1]
                    if flag == 1:
                        break
                    time.sleep(8)
            except:
                print(len(li))
                for i in range(0, len(li)):
                    f.write(str(li[i]) + '\r')
                print('error')

            for i in range(0, len(li)):
                f.write(str(li[i]) + '\r')
            print('writeover')
            f.close()

class Updatexag(CONNECTSQL):

     # type1, 2, 3,  4,  5:
    def get(self,count, tm):  # 1m,5m,15m,30m,60m qid: 6 agtd, 13 xag, 704 连续
        url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=13&type="+str(self.type)+"&count=" + str(
            count) + "&ts=" + str(tm)
        header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
        r = requests.post(url, headers=header)
        candle = json.loads(r.text)['data']['candle']
        li = []
        for i in range(0, len(candle)):
            li.append(tuple(candle[i].values()))
        #print(len(li))
        ts = li[0][7]  # 倒叙最新
        return li, ts




if __name__ == '__main__':

    con_sql = Updatexag('xag1d', 6, 214)
    con_sql.updatedb(con_sql.mydb)
    print('1d_over')
    con_sql = Updatexag('xag1h', 5, 140)
    con_sql.updatedb(con_sql.mydb)