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
import numpy as np
import matplotlib.pyplot as plt  # 重命名为plt

def draw(fag):
    exetend=[]
    for i in range(1, len(fag)):
        if fag[i][2] in ['空平', '多平']:
            exetend.append(fag[i] + [fag[i][10] - fag[i - 1][10]] + [fag[i - 1][11]])
    x, y = [], []
    for i in range(len(exetend)):
        y.append(exetend[i][-5])
        x.append(i)

    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)  # 1次多项式拟合
    p = np.poly1d(z)  # 将z转为多项式
    print(p)  # y=ax+b

    y1 = p(x)  # 打印出拟合的值

    plt.plot(x, y1, '-')
    plt.plot(x, y, '.', x, y1, '-r')  # '-r'表示用红线画出

    plt.show()
    print('--------------------------------------')
    return p

def get_MA(listc, timeperiod=13):
    ma = []
    for i in range(timeperiod, len(listc) + 1):
        ma.append(sum(listc[i - timeperiod:i]) / timeperiod)
    return ma

def getrate(ee):
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

def writeee(ee):
    if os.path.exists(r"d:\1.txt"):
        os.remove(r"d:\1.txt")
    with open(r"d:\1.txt", "a", encoding='utf-8') as f:
        title = '[总盈亏, 平仓盈亏, 开平方向, 开平点位, ma, o, c, h, l,time, 循环次数, 开仓延迟, 持仓,平仓利润率, 复利利润率, 最大浮盈, 最大浮亏, 持仓k数, 开仓延迟]'
        f.write(title + '\n')
        for i in range(0, len(ee)):
            f.write(format(ee[i]))
            f.write('\r')
    print('writeover')
    f.close()

def w_csv(ee, name='报表'):
    root = rf"d:\{name}.csv"
    with codecs.open(root, "w+", encoding='gbk') as f:
        headers = ['总盈亏', '平仓盈亏', '开平方向', '开平点位', 'ma', 'o', 'c', 'h', 'l', 'time', '循环次数', '开仓延迟', '持仓', '平仓利润率',
                   '复利利润率',
                   '最大浮盈', '最大浮亏', '持仓k数', '开仓延迟']
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(ee)
        f.flush()
        f.close()

class GetXag(object):
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
    def ot(self, bei, slope, ma_range, late_start, late, o, h, l, ts, c1):  # 主策略
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
        maxh, minl = 0, 10000
        CIrate, tax = 1, 0.00005
        for i in range(self.start_i, len(c)):  # 5900,2019-12-30 开始,结束 10600
            si = sign
            sign = round((ma[i] - ma[i - 1]) / ma[i - 1] * bei, 5)
            # log.append([si,sign])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if buy == 0 and sign > slope:  # and si > slope:   # or (bct == 1)
                lateb += 1
                # lates = 0
                sct = 0
                bct = 1
                log.append([lateb, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if sell == 1:  # 平空
                    sc = float(c[i])  # 正常损
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate += round(CIrate * self.__leve * ((so - sc) / so - tax), 4)

                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lates, chicang,
                         round((float(Dec(str(so)) - Dec(str(sc)))) / so, 4), CIrate, so - minl, so - maxh])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000
                lates = 0

                # 开多,low<ma_range收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (
                        late_start <= lateb <= late):  # and ma[i] >= ma[i - 1]
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) > o[i] and (
                            late_start <= lateb <= late):  # 低于ma开盘开仓
                        bo = o[i]

                    else:
                        bo = math.ceil(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))  # 19收+1开的ma价挂单开仓

                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    ee.append([float(e), '', '多开', bo, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lateb])
                    lateb, bct, buy = 0, 2, 1
                '''if buy == 1 and chicang == 0:
                    if l[i] <= ma[i] * 0.99:
                        bo = (bo + ma[i] * 0.99) / 2
                        print(e, '多追', tskc, lateb)
                        chicang += 1'''
            if sell == 0 and sign < -slope:  # and si < -slope and: # or sct == 1
                lates += 1
                # lateb = 0
                bct = 0
                sct = 1
                log.append([lates, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if buy == 1:
                    bc = float(c[i])
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo) / bo - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lateb, chicang,
                         round((float(Dec(str(bc)) - Dec(str(bo)))) / bo, 4), CIrate, maxh - bo, minl - bo])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000
                lateb = 0

                if h[i] >= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (
                        late_start <= lates <= late):  # and ma[i] <= ma[i - 1]:
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and (late_start <= lates <= late):
                        # elif lates == 2:
                        so = o[i]
                    # elif (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and lates == 1:
                    # so = c[i]
                    else:
                        so = math.floor(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))

                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    ee.append([float(e), '', '空开', so, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lates])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma[i] * 1.01:
                        so = (so + ma[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
        return ee, log, CIrate

class MIN1:
    def __init__(self, ma_range=30, table='ag1'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password',
            unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()

        sq = 'select c,h,l,ts,o from ' + table + ' order by ts'  # where ts>= 1635469260000
        d.execute(sq)
        a = d.fetchall()
        maxh, minl = -1, 100000
        c, h, l, ts, o = [], [], [], [], []
        # self.o.append(a[0][4])
        # self.ts.append(a[0][3])
        for i in range(0, len(a)):

            if a[i][3] % (1000 * 60 * ma_range) == 0:
                c.append(a[i - 1][0])
                h.append(maxh)
                l.append(minl)
                o.append(a[i][4])
                # self.ts.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( a[i-1][3]/ 1000)))
                ts.append(a[i - 1][3] + 60000)
                maxh, minl = -1, 100000
            if minl > a[i][2]: minl = a[i][2]
            if maxh < a[i][1]: maxh = a[i][1]
        self.o = o
        self.c = c[1:]
        self.h = h[1:]
        self.l = l[1:]
        self.ts = ts[1:]

# 16均线 15延迟
class Xag():
    def __init__(self, leve, table='xag1h', start_i=2):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()
        sq = 'select c,h,l,ts,o from ' + table + ' order by ts'  # +' where ts>1635346800000'
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

    # main bei扩展倍数 xie比较斜率 late延迟开仓k
    def ot(self, bei, slope, ma_range, late_start, late, o, h, l, ts, c1):  # 主策略
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
        maxh, minl = 0, 10000
        CIrate, tax = 1, 0.00005
        for i in range(self.start_i, len(c)):  # 5900,2019-12-30 开始,结束 10600
            si = sign
            sign = round((ma[i - 1] - ma[i - 2]) / ma[i - 2] * bei, 5)
            # log.append([si,sign])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if sign > slope and si>slope and buy == 0:  # or (bct == 1):
                lateb += 1
                lates = 0
                sct = 0
                bct = 1
                log.append([lateb, sign, si])
                if sell == 1:  # 平空
                    sc = (float(c[i - 1])*100)/100  # 正常损
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = ((Dec(str(e)) + Dec(str(so)) - Dec(str(sc)))*100)/100 * (chicang + 1)  # 平仓差额
                    CIrate += round(CIrate * self.__leve * ((so - sc) / so - tax), 4)

                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma[i - 1], o[i - 1], c[i - 1], h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, '', chicang,
                         round((float(Dec(str(so)) - Dec(str(sc)))) / so, 4), CIrate, so - minl, so - maxh])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000

                # 开多,low<19收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (
                        late_start <= lateb <= late):  # and ma[i] >= ma[i - 1]
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) > o[i] and (
                            late_start <= lateb <= late):  # 低于ma开盘开仓
                        bo = (o[i]*100)/100
                    else:
                        bo = ((round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))*100)/100  # 19收+1开的ma价挂单开仓
                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    ee.append([float(e), '', '多开', bo, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lateb])
                    lateb, bct, buy = 0, 2, 1
                '''if buy == 1 and chicang == 0:
                    if l[i] <= ma[i] * 0.99:
                        bo = (bo + ma[i] * 0.99) / 2
                        print(e, '多追', tskc, lateb)
                        chicang += 1'''
            if sign < -slope  and sell == 0 and si<-slope:  # or sct == 1:
                lates += 1
                lateb = 0
                bct = 0
                sct = 1
                log.append([lates, sign, si])
                if buy == 1:
                    bc = (float(c[i - 1])*100)/100
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = ((Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)))*100)/100 * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo) / bo - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma[i - 1], o[i - 1], c[i - 1], h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, '', chicang,
                         round((float(Dec(str(bc)) - Dec(str(bo)))) / bo, 4), CIrate, maxh - bo, minl - bo])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000

                if h[i] >= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (
                        late_start <= lates <= late):  # and ma[i] <= ma[i - 1]:
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and (late_start <= lates <= late):

                        so = (o[i]*100)/100
                    else:
                        so = ((round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))*100)/100
                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    ee.append([float(e), '', '空开', so, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lates])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma[i] * 1.01:
                        so = (so + ma[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
            # if ((sign < -xie and si < -xie )or (sign > xie and si > xie))==False:# and (sct == 1or bct == 1):
            # lateb, lates = 0, 0
        return ee, log, CIrate


    def inner(self, ts):
        a = int((ts / 1000 - 345600 + 3600 * 8) % (86400) / 3600)
        list = [9, 10, 11, 1, 2, 3, 21, 22, 23, 0, 1, 2]
        if a in list:
            return True
        else:
            return False


class f_mod(GetXag):
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
    def ot(self, bei, slope, ma_range, late_start, late, o, h, l, ts, c1):  # 主策略
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
        maxh, minl = 0, 10000
        CIrate, tax = 1, 0.00005
        for i in range(self.start_i, len(c)):  # 5900,2019-12-30 开始,结束 10600
            si = sign
            sign = round((ma[i - 1] - ma[i - 2]) / ma[i - 2] * bei, 5)
            log.append(
                [sign, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), l[i - 1], ma[i - 1]])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if sign > slope and si > slope and buy == 0:  # or (bct == 1)
                lateb += 1
                lates = 0
                sct = 0
                bct = 1
                # log.append([lateb, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if sell == 1:  # 平空
                    sc = float(c[i - 1])  # 正常损
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate += round(CIrate * self.__leve * ((so - sc) / so - tax), 4)

                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma[i - 1], o[i - 1], c[i - 1],
                         h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, lates, chicang,
                         round((float(Dec(str(so)) - Dec(str(sc)))) / so, 4), CIrate, so - minl, so - maxh])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000

                # 开多,low<ma_range收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (
                        late_start <= lateb <= late):  # and ma[i] >= ma[i - 1]
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) > o[i] and (
                            late_start <= lateb <= late):  # 低于ma开盘开仓
                        bo = o[i]

                    else:
                        bo = math.ceil(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))  # 19收+1开的ma价挂单开仓

                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    ee.append([float(e), '', '多开', bo, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lateb])
                    lateb, bct, buy = 0, 2, 1
                '''if buy == 1 and chicang == 0:
                    if l[i] <= ma[i] * 0.99:
                        bo = (bo + ma[i] * 0.99) / 2
                        print(e, '多追', tskc, lateb)
                        chicang += 1'''
            if sign < -slope and si < -slope and sell == 0:  # or sct == 1
                lates += 1
                lateb = 0
                bct = 0
                sct = 1
                # log.append([lates, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if buy == 1:
                    bc = float(c[i - 1])
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo) / bo - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma[i - 1], o[i - 1], c[i - 1],
                         h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, lateb, chicang,
                         round((float(Dec(str(bc)) - Dec(str(bo)))) / bo, 4), CIrate, maxh - bo, minl - bo])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000

                if h[i] >= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (
                        late_start <= lates <= late):  # and ma[i] <= ma[i - 1]:
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and (late_start <= lates <= late):
                        # elif lates == 2:
                        so = o[i]
                    # elif (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and lates == 1:
                    # so = c[i]
                    else:
                        so = math.floor(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))

                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    ee.append([float(e), '', '空开', so, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lates])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma[i] * 1.01:
                        so = (so + ma[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
            # if ((sign < -xie and si < -xie )or (sign > xie and si > xie))==False:# and (sct == 1or bct == 1):
            # lateb, lates = 0, 0
        return ee, log, CIrate


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
    def ot(self, bei, slope, ma_range, late_start, late, o, h, l, ts, c1):  # 主策略
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
        for i in range(self.start_i, len(c)):  # 5900,2019-12-30 开始,结束 10600
            si = sign
            sign = round((ma[i - 1] - ma[i - 2]) / ma[i - 2] * bei, 5)
            log.append(
                [sign, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), l[i - 1], ma[i - 1]])
            if h[i] > maxh and (sell == 1 or buy == 1):
                maxh = h[i]
            if l[i] < minl and (sell == 1 or buy == 1):
                minl = l[i]
            # 前1角and前2角>xie,且空仓,或有过信号
            if sign > slope and si>slope and buy == 0:  # or (bct == 1)
                lateb += 1
                lates = 0
                sct = 0
                bct = 1
                # log.append([lateb, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if sell == 1 :# and si > slope:  # 平空
                    sc = float(c[i - 1])  # 正常损
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate += round(CIrate * self.__leve * ((so - sc) / so - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma[i - 1], o[i - 1], c[i - 1],
                         h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, lates, chicang,
                         round((float(Dec(str(so)) - Dec(str(sc)))) / so, 4), CIrate, so - minl, so - maxh])
                    # print(e, '空平',sc,ts[i],si,sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 100000

                # 开多,low<ma_range收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (
                        late_start <= lateb <= late):  # and ma[i] >= ma[i - 1]
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) > o[i] and (
                            late_start <= lateb <= late):  # 低于ma开盘开仓
                        bo = o[i]
                    else:
                        bo = math.ceil(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))  # 19收+1开的ma价挂单开仓
                    tskc = ts[i]
                    # print(e, '多开',bo, tskc, lateb,si,sign)
                    ee.append([float(e), '', '多开', bo, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lateb])
                    lateb, bct, buy = 0, 2, 1
                '''if buy == 1 and chicang == 0:
                    if l[i] <= ma[i] * 0.99:
                        bo = (bo + ma[i] * 0.99) / 2
                        print(e, '多追', tskc, lateb)
                        chicang += 1'''
            if sign < -slope and si<-slope and sell == 0:  # or sct == 1
                lates += 1
                lateb = 0
                bct = 0
                sct = 1
                # log.append([lates, sign, si, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if buy == 1 :# and si < -slope:
                    bc = float(c[i - 1])
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo) / bo - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma[i - 1], o[i - 1], c[i - 1],
                         h[i - 1], l[i - 1],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i - 1] / 1000)), i - 1, lateb, chicang,
                         round((float(Dec(str(bc)) - Dec(str(bo)))) / bo, 4), CIrate, maxh - bo, minl - bo])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 100000

                if h[i] >= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (
                        late_start <= lates <= late):  # and ma[i] <= ma[i - 1]:
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and (late_start <= lates <= late):
                        # elif lates == 2:
                        so = o[i]
                    # elif (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and lates == 1:
                    # so = c[i]
                    else:
                        so = math.floor(round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3))

                    tskc = ts[i]
                    # print(e, '空开', so,tskc, lates,si,sign)
                    ee.append([float(e), '', '空开', so, ma[i], o[i], c[i], h[i], l[i],
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, lates])
                    # print(bo, bc, so, sc, o[i], c[i], h[i], l[i], round(ma[i], 2))
                    # input()
                    lates, sct, sell = 0, 2, 1
                '''if sell == 1 and chicang == 0:
                    if h[i] >= ma[i] * 1.01:
                        so = (so + ma[i] * 1.01) / 2
                        print(e, '空追', tskc, lates)
                        chicang += 1'''
            # if ((sign < -xie and si < -xie )or (sign > xie and si > xie))==False:# and (sct == 1or bct == 1):
            # lateb, lates = 0, 0
        return ee, log, CIrate
