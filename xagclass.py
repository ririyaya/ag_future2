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


# 16均线 15延迟

class GetXag:
    def __init__(self,leve,table='ag15'): #杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password')  # 'caching_sha2_password')  #
        d = mydb.cursor()

        sq = 'select c,h,l,ts,o from '+table  # where ts>1609893464000'
        d.execute(sq)
        a = d.fetchall()
        c1, h, l, ts, o = [], [], [], [], []
        for i in range(0, len(a)):
            c1.append(round(a[i][0], 5))
            h.append(round(a[i][1], 5))
            l.append(round(a[i][2], 5))
            ts.append(a[i][3])
            o.append(round(a[i][4], 5))

        self.c1=c1
        self.__leve=leve
        self.c = c1[19:]
        self.h = h[19:]
        self.l = l[19:]
        self.ts = ts[19:]
        self.o = o[19:]

    # main
    def ot(self, bei, xie, late_start,late, o, c, h, l, ts, c1,ma_range):  # 主策略
        ma20 = talib.MA(np.array(c1), timeperiod=ma_range)[19:]
        ee = []
        log = []
        chicang = 0
        lateb, lates = 0, 0
        si, sign, e = 0, 0, 0
        bct, sct, bo, bc, so, sc, buy, sell = 0, 0, 0, 0, 0, 0, 0, 0
        maxh, minl = 0, 10000
        CIrate ,tax= 1,0.0001
        for i in range(0, len(c)):  # 5900,2019-12-30
            si = sign
            sign = round((ma20[i] - ma20[i - 1]) / ma20[i - 1] * bei, 5)
            # log.append([si,sign])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if (sign > xie and si > xie and buy == 0) or (bct == 1):
                lateb += 1
                lates = 0
                sct = 0
                if sell == 1:  # 平空
                    sc = float(c[i])  # 正常损
                    # if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate+=round(CIrate * self.__leve * ((so-sc)/so - tax),4)
                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma20[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '', chicang,round((float(Dec(str(so)) - Dec(str(sc))))/so,4),CIrate])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000
                bct = 1
                # 开多,low<19收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (late_start < lateb <= late) and ma20[i] >= ma20[i - 1]:
                    if round(ma20[i], 3) > o[i]:  # 低于ma开盘开仓
                        bo = math.ceil(o[i])
                    elif lateb == 1:
                        bo = math.ceil(o[i])
                    else:
                        bo = math.ceil(round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3))  # 19收+1开的ma价挂单开仓
                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    ee.append([float(e), '', '多开', bo, ma20[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, (lateb - 1)])
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
                    # if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo)/bo - tax),4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma20[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '',  chicang,round((float(Dec(str(bo)) - Dec(str(bc))))/so,4),CIrate])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000
                sct = 1
                if h[i] >= (round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (late_start < lates <= late) and ma20[i] <= ma20[i - 1]:
                    if round(ma20[i], 3) < o[i]:
                        so = math.floor(o[i])
                    elif lates == 1:
                        so = math.floor(o[i])
                    else:
                        so = math.floor(round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3))
                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    ee.append([float(e), '', '空开', so, ma20[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, (lates - 1)])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma20[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma20[i] * 1.01:
                        so = (so + ma20[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
        return ee, log

    def getrate(self, ee):
        rat = []
        i = 1
        while i < len(ee):
            rat.append(round(ee[i][1] / ee[i - 1][3], 5))
            i += 2

        torat1 = 0
        for i in range(len(rat)):
            if rat[i] > 0:
                torat1 += 1
        return round(torat1 / len(rat), 4)

    def writeee(self, ee):
        if os.path.exists(r"d:\1.txt"):
            os.remove(r"d:\1.txt")
        with open(r"d:\1.txt", "a", encoding='utf-8') as f:
            for i in range(0, len(ee)):
                f.write(format(ee[i]))
                f.write('\r')
        print('writeover')
        f.close()



class Xag():
    def __init__(self,leve,table='xag1h'): #杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password')  # 'caching_sha2_password')  #
        d = mydb.cursor()

        sq = 'select c,h,l,ts,o from '+table  # where ts>1609893464000'
        d.execute(sq)
        a = d.fetchall()
        c1, h, l, ts, o = [], [], [], [], []
        for i in range(0, len(a)):
            c1.append(round(a[i][0], 5))
            h.append(round(a[i][1], 5))
            l.append(round(a[i][2], 5))
            ts.append(a[i][3])
            o.append(round(a[i][4], 5))

        self.c1=c1
        self.__leve=leve #Leverage杠杆
        self.c = c1[19:]
        self.h = h[19:]
        self.l = l[19:]
        self.ts = ts[19:]
        self.o = o[19:]

    # main bei扩展倍数 xie比较斜率 late延迟开仓k
    def ot(self, bei, xie, late_start,late, o, c, h, l, ts, c1,ma_range):  # 主策略
        ma20 = talib.MA(np.array(c1), timeperiod=ma_range)[19:]
        xagfag=[]
        ee = []
        chicang = 0
        lateb, lates = 0, 0
        si, sign, e = 0, 0, 0
        bct, sct, bo, bc, so, sc, buy, sell = 0, 0, 0, 0, 0, 0, 0, 0
        maxh, minl = 0, 10000
        CIrate ,tax= 1,0.0001 #复利利润比,手续费
        for i in range(0, len(c)):  # 5900,2019-12-30
            si = sign
            sign = round((ma20[i] - ma20[i - 1]) / ma20[i - 1] * bei, 5)
            # log.append([si,sign])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if (sign > xie and si > xie and buy == 0) or (bct == 1):
                lateb += 1
                lates = 0
                sct = 0
                if sell == 1 and self.inner(ts[i]):  # 平空
                    sc = float(c[i])  # 正常损
                    # if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate+=CIrate * self.__leve * ((so-sc)/so - tax)
                    xagfag.append(['空平', sc, ma20[i], maxh, minl, h[i], l[i],ts[i]])
                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, round(ma20[i],4), o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '', chicang,(float(Dec(str(so)) - Dec(str(sc))))/so,round(CIrate,4)])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000
                bct = 1
                # 开多,low<19收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (late_start < lateb <= late) and  ma20[i] >= ma20[i - 1] and self.inner(ts[i]):
                    if round(ma20[i], 3) > o[i] :  # 低于ma开盘开仓
                        bo = o[i]
                    elif lateb == 1:
                        bo = o[i]
                    else:
                        bo = round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)  # 19收+1开的ma价挂单开仓
                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    xagfag.append(['多开', bo, ma20[i], maxh, minl, h[i], l[i],ts[i]])
                    ee.append(
                        [float(e), '', '多开', bo, round(ma20[i],4), o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, (lateb - 1)])
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
                if buy == 1 and self.inner(ts[i]):
                    bc = float(c[i])
                    # if round(abs(o[i]-ma20[i-1])/ma20[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += CIrate * self.__leve * ((bc - bo)/bo - tax)
                    xagfag.append(['多平', bc, ma20[i], maxh, minl, h[i], l[i],ts[i]])
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, round(ma20[i],4), o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '', chicang,(float(Dec(str(bc)) - Dec(str(bo))))/bo,round(CIrate,4)])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000
                sct = 1
                if h[i] >= (round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (late_start < lates <= late) and ma20[i] <= ma20[i - 1]and self.inner(ts[i]):

                    if round(ma20[i], 3) < o[i] :
                        so = (o[i])
                    elif lates == 1:
                        so = (o[i])
                    else:
                        so = round(ma20[i], 3) - round((c[i] - o[i]) / ma_range, 3)
                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    xagfag.append(['空开', so, ma20[i], maxh, minl, h[i], l[i],ts[i]])
                    ee.append([float(e), '', '空开', so, round(ma20[i],4), o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, (lates - 1)])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma20[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma20[i] * 1.01:
                        so = (so + ma20[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
        return ee, xagfag,CIrate

    def getrate(self, ee):
        rat = []
        i = 1
        while i < len(ee):
            rat.append(round(ee[i][1] / ee[i - 1][3], 5))
            i += 2
        torat1 = 0
        for i in range(len(rat)):
            if rat[i] > 0:
                torat1 += 1
        return round(torat1 / len(rat), 4)

    def inner(self,ts):
        a = int((ts / 1000 - 345600 + 3600 * 8) % (86400) / 3600)
        list=[9,10,11,1,2,3,21,22,23,0,1,2]
        if a  in list:
            return True
        else:
            return False
