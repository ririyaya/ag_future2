import trend
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

con_sql = Updatexag('xag1h', 5, 114)
#con_sql.updatedb(con_sql.mydb)
# con_sql.updatetxt()


if os.path.exists(r"d:\2.txt"):
    os.remove(r"d:\2.txt")
f = open(r"d:\2.txt", "a", encoding='utf-8')
# m1=xagclass.MIN1(15)
f_ag = trend.Xag(1, 'xag1h', 2)  # 杠杆倍率,表,强制循环起点

for ma_range in range(16, 17):
    for maxlate in range(15, 26):
        for slope in range(5, 6):  # 斜率?
            for minlate in range(2, 3):  # startlate
                fag, log, CIrate = f_ag.ot(100000, slope, ma_range, minlate, maxlate, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
                # fag, log, CIrate = f_ag.ot(100000, k, 2, j, m1.o, m1.h, m1.l, m1.ts, m1.c, i)
                tex = (ma_range, minlate, maxlate, slope, len(fag) / 2, fag[-1][0], trend.getrate(fag), round(CIrate, 3))
                #qushihuitiao.writeee(fag)
                print(tex)
                #print(fag[-2])
                #print(fag[-1])
                # print(log[-1])
                f.write(str(tex) + '\r')

exetend=[]
for i in range(1,len(fag)):
    if fag[i][2] in ['空平','多平']:
        exetend.append(fag[i]+[fag[i][10]-fag[i-1][10]]+[fag[i-1][11]])

trend.w_csv(exetend, '报表扩展')
trend.w_csv(fag, '报表')



'''
f_ag = xagmod(3, 'ag15mod' )
for ma_range in range(55, 66):
    for maxlate in range(25, 26):
        for slope in range(5, 6):  # 斜率?
            for minlate in range(2, 3):  # startlate
                fag, log, CIrate = f_ag.ot(100000, 5, ma_range, 2, 25, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1, f_ag.sio)
                # fag, log, CIrate = f_ag.ot(100000, k, 2, j, m1.o, m1.h, m1.l, m1.ts, m1.c, i)
                tex = (ma_range, minlate, maxlate, slope, len(fag) / 2, fag[-1][0],  round(CIrate, 3))
                #qushihuitiao.writeee(fag)
                print(tex)
                #print(fag[-2])
                print(fag[-1])
                # print(log[-1])
                f.write(str(tex) + '\r')
'''