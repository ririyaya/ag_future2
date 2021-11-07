import qushihuitiao
import math
import os
import time
from decimal import Decimal as Dec
from decimal import getcontext
import mysql.connector
import numpy as np
import talib

from updatedb import Updatexag
#16均线 15延迟

#con_sql = Updatexag('xag1h', 5, 114)
#con_sql.updatedb(con_sql.mydb)
# con_sql.updatetxt()


if os.path.exists(r"d:\2.txt"):
    os.remove(r"d:\2.txt")
f = open(r"d:\2.txt", "a", encoding='utf-8')
# m1=xagclass.MIN1(15)
f_ag = qushihuitiao.Xag(1, 'xag1h', 0)  # 杠杆倍率,表,强制循环起点
"""
for ma_range in range(16, 17):
    for maxlate in range(25, 26):
        for slope in range(5, 6):  # 斜率?
            for minlate in range(2, 3):  # startlate
                fag, log, CIrate = f_ag.ot(100000, slope, ma_range, minlate, maxlate, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
                # fag, log, CIrate = f_ag.ot(100000, k, 2, j, m1.o, m1.h, m1.l, m1.ts, m1.c, i)
                tex = (ma_range, minlate, maxlate, slope, len(fag) / 2, fag[-1][0], qushihuitiao.getrate(fag), round(CIrate, 3))
                #qushihuitiao.writeee(fag)
                print(tex)
                #print(fag[-2])
                #print(fag[-1])
                # print(log[-1])
                f.write(str(tex) + '\r')
"""
# macag=xagclass.mac_ag(12,1,'ag30')
# maag,log=macag.ot( 100000, 5, 2, 15, 12)
title = '[总盈亏, 平仓盈亏, 开平方向, 开平点位, ma, o, c, h, l,time, 循环次数, 开仓延迟, 持仓,平仓利润率, 复利利润率, 最大浮盈, 最大浮亏]'

fag, log, CIrate = f_ag.ot(100000, 5, 16, 2, 15, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
dt={}
for i in range(len(fag)):
    dt[int(time.mktime(time.strptime(fag[i][9], "%Y-%m-%d %H:%M:%S"))*1000)]=fag[i][2]


class xagmod(qushihuitiao.GetXag):
    # main
    def ot(self, bei, slope, ma_range, late_start, late, o, h, l, ts, c1,dt):  # 主策略
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
            if sign > slope and si > slope and buy == 0 :
                if int(ts[i]/1000%86400/3600) in dt:
                    print('in')
                lateb += 1
                lates = 0
                sct = 0
                bct = 1
                log.append([lateb, sign, si,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if sell == 1 and int(ts[i]/1000%86400/3600) in dt and dt[int(ts[i]/1000%86400/3600) ]=='平空':  # 平空
                    sc = float(c[i])  # 正常损
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#偏离值过4%损
                    # sc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(so)) - Dec(str(sc)), 5) * (chicang + 1)  # 平仓差额
                    CIrate += round(CIrate * self.__leve * ((so - sc) / so - tax), 4)

                    ee.append(
                        [float(e), float(Dec(str(so)) - Dec(str(sc))), '空平', sc, ma[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '', chicang,
                         round((float(Dec(str(so)) - Dec(str(sc)))) / so, 4), CIrate, so - minl, so - maxh])
                    # print(e, '空平',sc,ts[i],si,sign)
                    # print(bo, bc, so, sc, si, sign)
                    lates, sell, chicang, maxh, minl = 0, 0, 0, 0, 10000

                # 开多,low<19收+1开的ma,前1ma>=前2ma
                if l[i] <= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and buy == 0 and (
                        late_start<=lateb <= late) and int(ts[i]/1000%86400/3600) in dt and dt[int(ts[i]/1000%86400/3600) ]=='多开':  # and ma[i] >= ma[i - 1]
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
            if sign < -slope and si < -slope and sell == 0 :  #or sct == 1
                lates += 1
                lateb = 0
                bct = 0
                sct = 1
                log.append([lates, sign, si,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000))])
                if buy == 1 and int(ts[i]/1000%86400/3600) in dt and dt[int(ts[i]/1000%86400/3600) ]=='多平':
                    bc = float(c[i])
                    # if round(abs(o[i]-ma[i-1])/ma[i-1],4)>0.04:#
                    # bc=float(o[i])
                    e = round(Dec(str(e)) + Dec(str(bc)) - Dec(str(bo)), 5) * (chicang + 1)
                    CIrate += round(CIrate * self.__leve * ((bc - bo) / bo - tax), 4)
                    ee.append(
                        [float(e), float(Dec(str(bc)) - Dec(str(bo))), '多平', bc, ma[i], o[i], c[i], h[i], l[i],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[i] / 1000)), i, '', chicang,
                         round((float(Dec(str(bc)) - Dec(str(bo)))) / bo, 4), CIrate, maxh - bo, minl - bo])
                    # print(e, '多平', bc,ts[i],si,sign)
                    # print(bo, bc, so, sc)
                    # input()
                    lateb, buy, chicang, maxh, minl = 0, 0, 0, 0, 10000

                if h[i] >= (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) and sell == 0 and (
                        late_start <= lates <= late) and int(ts[i]/1000%86400/3600) in dt and dt[int(ts[i]/1000%86400/3600) ]=='空开':  # and ma[i] <= ma[i - 1]:
                    if (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and (late_start <= lates <= late):
                        # elif lates == 2:
                        so = o[i]
                    #elif (round(ma[i], 3) - round((c[i] - o[i]) / ma_range, 3)) < o[i] and lates == 1:
                        #so = c[i]
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

f_ag = xagmod(3, 'ag30', 0 )
fag, log, CIrate = f_ag.ot(100000, 5, 13, 2, 25, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1,dt)
print(len(fag))
f.close()
