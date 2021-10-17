import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
import talib
from decimal import Decimal as Dec
from decimal import getcontext

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="111",
    database='koudai',  # 数据库
    auth_plugin='mysql_native_password')  # 'caching_sha2_password')  #
d = mydb.cursor()

sq = 'select c,h,l,t,o from ag1d '# where ts<1584635280000'
d.execute(sq)
a = d.fetchall()
c1, h, l, ts, o = [], [], [], [], []
for i in range(0, len(a)):
    c1.append(round(a[i][0], 5))
    h.append(round(a[i][1], 5))
    l.append(round(a[i][2], 5))
    ts.append(a[i][3])
    o.append(round(a[i][4], 5))

ma20 = talib.MA(np.array(c1), timeperiod=20)[19:]
c = c1[19:]
h = h[19:]
l = l[19:]
ts = ts[19:]
o = o[19:]


print('#')


def ot(bei, xie, late=20):  # 主策略
    ee = []
    log = []
    chicang = 0
    lateb, lates = 0, 0
    si, sign, e = 0, 0, 0
    bct, sct, bo, bc, so, sc, buy, sell = 0, 0, 0, 0, 0, 0, 0, 0
    maxh,minl=0,10000
    for i in range(0, len(c)):  # 5900,2019-12-30
        si = sign
        sign = round((ma20[i] - ma20[i - 1]) / ma20[i-1] * bei, 5)
        #log.append([si,sign])
        if h[i] > maxh and (sell==1 or buy==1):
            maxh = h[i]
        if l[i] < minl and (sell==1 or buy==1):
            minl = l[i]
        # 前1角and前2角>xie,且空仓,或有过信号
        if (sign > xie and si > xie and buy == 0) or (bct == 1):
            lateb += 1
            lates = 0
            sct = 0
            if sell == 1:#平空
                sc = float(c[i])#正常损
                if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#偏离值过4%损
                    sc=float(o[i])
                e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)),5)*(chicang+1)#平仓差额
                ee.append(
                    [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma20[i], o[i], c[i], h[i], l[i], ts[i], i,'',chicang,maxh,minl])
                print(e, '空平',ts[i], chicang,si,sign)
                # print(bo, bc, so, sc, si, sign)
                lates, sell, chicang ,maxh,minl= 0, 0, 0,0,10000
            bct = 1
            # 开多,low<19收+1开的ma,前1ma>=前2ma
            if  buy == 0  and (lateb <= late):
                bo = o[i]
                tskc = ts[i]
                print(e, '多开', tskc, lateb,si,sign,sct)
                ee.append([float(e), '', '多开', bo, ma20[i], o[i], c[i], h[i], l[i], ts[i], i, (lateb-1)])
                lateb, bct, buy = 0, 2, 1
            '''if buy == 1 and chicang == 0:
                if l[i] <= ma20[i] * 0.99:
                    bo = (bo + ma20[i] * 0.99) / 2
                    print(e, '多追', tskc, lateb)
                    chicang += 1'''
        if (sign < -xie and si < -xie and sell == 0) or sct == 1:
            lates += 1
            lateb = 0
            bct = 0
            if buy == 1:
                bc = float(c[i])
                if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#
                    bc=float(o[i])
                e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)),5)*(chicang+1)
                ee.append(
                    [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma20[i], o[i], c[i], h[i], l[i],ts[i], i,'',chicang,maxh,minl])
                print(e, '多平', ts[i],chicang,si,sign,sct)
                #print(bo, bc, so, sc)
                # input()
                lateb,buy, chicang,maxh,minl= 0, 0, 0,0,10000
            sct = 1
            if sell == 0 and (lates <= late):
                so = o[i]
                tskc = ts[i]
                print(e, '空开', tskc, lates,si,sign)
                ee.append([float(e),'', '空开', so, ma20[i], o[i], c[i], h[i], l[i], ts[i], i,(lates-1)])
                # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma20[i], 2))
                # input()
                lates, sct, sell = 0, 2, 1
            '''if sell == 1 and chicang == 0:
                if h[i] >= ma20[i] * 1.01:
                    so = (so + ma20[i] * 1.01) / 2
                    print(e, '空追', tskc, lates)
                    chicang += 1'''
    return ee, log


ee, log = ot(10000, 5, 60)
print(len(ee)/2, ee[-1])
def writeee(ee,f):
    for i in range(0,len(ee)):
        f.write(format(ee[i]))
        f.write('\r')

with open(r"C:\Users\16242\Desktop\1.txt", "a", encoding='utf-8') as f:
    #writeee(ee,f)
    f.close()

'''
for i in range(20,21):
    ma20 = talib.MA(np.array(c1), timeperiod=i)[19:]
    ee, log = ot(100000, 5, 18)
    with open(r"C:/Users\16242\Desktop\1.txt", "a", encoding='utf-8') as fi:
        fi.write(str(len(ee)/2)+str(ee[-1])+'\n')
    #fi.close()
'''