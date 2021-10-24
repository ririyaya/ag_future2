import requests
import re
import json
import time
import mysql.connector
import math
import numpy as np
import talib
from decimal import Decimal as Dec
from decimal import getcontext
import os

#16均线 15延迟


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="111",
    database='koudai',  # 数据库
    auth_plugin='mysql_native_password')  # 'caching_sha2_password')  #
d = mydb.cursor()

sq = 'select c,h,l,ts,o from xag1h'#  where ts>1609893464000'
d.execute(sq)
a = d.fetchall()
c1, h, l, ts, o = [], [], [], [], []
for i in range(0, len(a)):
    c1.append(round(a[i][0], 5))
    h.append(round(a[i][1], 5))
    l.append(round(a[i][2], 5))
    ts.append(a[i][3])
    o.append(round(a[i][4], 5))

ma20 = talib.MA(np.array(c1), timeperiod=16)[19:]
c = c1[19:]
h = h[19:]
l = l[19:]
ts = ts[19:]
o = o[19:]


print('#')

#main
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
                #if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#偏离值过4%损
                    #sc=float(o[i])
                e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)),5)*(chicang+1)#平仓差额
                ee.append(
                    [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma20[i], o[i], c[i], h[i], l[i], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)), i,'',chicang,maxh,minl,(float(Dec(str(so)) - Dec(str(sc))))/so])
                print(e, '空平',sc,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)),si,sign)
                # print(bo, bc, so, sc, si, sign)
                lates, sell, chicang ,maxh,minl= 0, 0, 0,0,10000
            bct = 1
            # 开多,low<19收+1开的ma,前1ma>=前2ma
            if l[i] <= (round(ma20[i], 3) - round((c[i] - o[i]) / 16, 3)) and buy == 0  and (1<lateb <= late)and ma20[i]>=ma20[i-1]:
                if round(ma20[i], 3) > o[i]:#低于ma开盘开仓
                    bo = o[i]
                elif lateb==1:
                    bo = c[i]
                else:
                    bo = round(ma20[i], 3) - round((c[i] - o[i]) / 16, 3)#19收+1开的ma价挂单开仓
                tskc = ts[i]
                print(e, '多开',bo,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)), tskc, lateb,si,sign)
                ee.append([float(e), '', '多开', bo, ma20[i], o[i], c[i], h[i], l[i], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)), i, (lateb-1)])
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
                #if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#
                    #bc=float(o[i])
                e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)),5)*(chicang+1)
                ee.append(
                    [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma20[i], o[i], c[i], h[i], l[i],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)), i,'',chicang,maxh,minl,(float(Dec(str(bc)) - Dec(str(bo))))/bo])
                print(e, '多平', bc,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)),si,sign)
                #print(bo, bc, so, sc)
                # input()
                lateb,buy, chicang,maxh,minl= 0, 0, 0,0,10000
            sct = 1
            if h[i] >= (round(ma20[i], 3) - round((c[i] - o[i]) / 16, 3)) and sell == 0 and (1<lates <= late) and ma20[i]<=ma20[i-1]:
                if round(ma20[i], 3) < o[i]:
                    so = o[i]
                elif lates==1:
                    so=c[i]
                else:
                    so = round(ma20[i], 3) - round((c[i] - o[i]) / 16, 3)
                tskc = ts[i]
                print(e, '空开', so,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)),tskc, lates,si,sign)
                ee.append([float(e),'', '空开', so, ma20[i], o[i], c[i], h[i], l[i], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts[i])/1000)), i,(lates-1)])
                # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma20[i], 2))
                # input()
                lates, sct, sell = 0, 2, 1
            '''if sell == 1 and chicang == 0:
                if h[i] >= ma20[i] * 1.01:
                    so = (so + ma20[i] * 1.01) / 2
                    print(e, '空追', tskc, lates)
                    chicang += 1'''
    return ee, log


def getrate(ee):
    rat=[]
    i=1
    while i<len(ee):
        rat.append(round(ee[i][1]/ee[i-1][3],5))
        i+=2

    torat1=0
    for i in range(len(rat)):
        if rat[i]>0:
            torat1+=1
    return round(torat1/len(rat),4)


def writeee(ee,f):
    for i in range(0,len(ee)):
        #f.write(format(ee[i]))
        f.write('\r')

os.remove(r"D:\1.txt")
with open(r"D:\1.txt", "a", encoding='utf-8') as f:
    #ee, log = ot(100000, 5, 15)
    #writeee(ee,f)
    f.close()

with open(r"D:\1.txt", "a", encoding='utf-8') as fi:
    '''
    for i in range(13,27):
        ma20 = talib.MA(np.array(c1), timeperiod=i)[19:]
        for j in range(10,40):
            print(i,j)
            ee, log = ot(100000, 5, j)
            fi.write(str(len(ee)/2)+str(ee[-1])+'#')
            fi.write(str(getrate(ee))+'#')
            fi.write(str(i) +'#'+ str(j) + '\r')'''
fi.close()


def writeee(ee):
    if os.path.exists(r"D:\1.txt"):
        os.remove(r"D:\1.txt")
    with open(r"D:\1.txt", "a", encoding='utf-8') as f:
        for i in range(0, len(ee)):
            f.write(format(ee[i]))
            f.write('\r')
    f.close()

ee, log = ot(100000, 5, 15)
print(len(ee)/2, ee[-1])
#writeee(ee)
print(getrate(ee))

