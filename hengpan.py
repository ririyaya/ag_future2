import json
import math
import os
import re
import time
from decimal import Decimal as Dec
from decimal import getcontext
import mysql.connector
import numpy as np
import requests
import talib
import csv
import codecs

class k_mod(object):
    def __init__(self, leve, table='ag15', start_i=2, ):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()
        sq = 'select c,h,l,ts,o from ' + table + ' group by c,h,l,ts,o  order by ts'  # +' where ts>1635346800000'
        d.execute(sq)
        a = d.fetchall()
        self.c1, self.h, self.l, self.ts, self.o = [], [], [], [], []
        for i in range(0, len(a)):
            self.c1.append(round(a[i][0], 5))
            self.h.append(round(a[i][1], 5))
            self.l.append(round(a[i][2], 5))
            self.ts.append(a[i][3])
            self.o.append(round(a[i][4], 5))
        self.start_i = start_i
        self.__leve = leve

    # main
    def ot(self, env_range, ma_range,  o, h, l, ts, c1):  # 主策略
        c = c1[ma_range - 1:]
        h = h[ma_range - 1:]
        l = l[ma_range - 1:]
        ts = ts[ma_range - 1:]
        o = o[ma_range - 1:]
        ma = talib.MA(np.array(c1, dtype=np.float64), timeperiod=ma_range)[ma_range - 1:]
        ee, log = [], []
        lateb, lates, chicang = 0, 0, 0
        si, sign, e = 0, 0, 0
        bct, sct, bo, bc, so, sc, buy, sell = 0, 0, 0, 0, 0, 0, 0, 0
        maxh, minl = 0, 100000
        CIrate, tax = 1, 0.00005
        for i in range(0, len(c)):  # 5900,2019-12-30 开始,结束 10600
            env =range(math.ceil(ma[i]*(1-0.01*env_range)),math.floor(ma[i]*(1+0.01*env_range)))
            if c[i] in env:
                log.append(i)
        return log,ma
'''
f_ag = k_mod(2, 'ag30')  # 杠杆倍率,表,强制循环起点
for ma_range in range(20,21):
    for slope in [2]:
        fag,ma= f_ag.ot(slope, ma_range,  f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
        print(len(fag)/len(f_ag.o))

lx=[]
for i in range(len(fag)-1):
    if fag[i+1]-fag[i]!=1:
        lx.append(i)
print(len(lx))
lo=0
for i in range(len(lx)-1):
    if lx[i+1]-lx[i]!=1:
        lo+=1
print(lo)'''

min_l,max_h=10000,0
range=5
if kbar[i-1]['l']>min_l and kbar[i-1]['h']<max_h:
    henpan=True

kbar =[[o,c,h,l,i],[o,c,h,l,i]]

min_l=kbar[i]['l'] if kbar[i]['l']<min_l else min_l
max_h=kbar[i]['h'] if kbar[i]['h']>max_h else max_h

