import qushihuitiao
import os
from updatedb import Updatexag
#16均线 15延迟

con_sql = Updatexag('xag1h', 5, 114)
con_sql.updatedb(con_sql.mydb)
# con_sql.updatetxt()


if os.path.exists(r"d:\2.txt"):
    os.remove(r"d:\2.txt")
f = open(r"d:\2.txt", "a", encoding='utf-8')
# m1=xagclass.MIN1(15)
f_ag = qushihuitiao.Xag(1, 'xag1h', 0)  # 杠杆倍率,表,强制循环起点
for ma_range in range(16, 17):
    for maxlate in range(25, 26):
        for slope in range(5, 6):  # 斜率?
            for minlate in range(2, 3):  # startlate
                fag, log, CIrate = f_ag.ot(100000, slope, ma_range, minlate, maxlate, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
                # fag, log, CIrate = f_ag.ot(100000, k, 2, j, m1.o, m1.h, m1.l, m1.ts, m1.c, i)
                tex = (ma_range, minlate, maxlate, slope, len(fag) / 2, fag[-1][0], qushihuitiao.getrate(fag), round(CIrate, 3))
                #xagclass.writeee(fag)
                print(tex)
                print(fag[-2])
                print(fag[-1])
                # print(log[-1])
                f.write(str(tex) + '\r')

# macag=xagclass.mac_ag(12,1,'ag30')
# maag,log=macag.ot( 100000, 5, 2, 15, 12)
title = '[总盈亏, 平仓盈亏, 开平方向, 开平点位, ma, o, c, h, l,time, 循环次数, 开仓延迟, 持仓,平仓利润率, 复利利润率, 最大浮盈, 最大浮亏]'

"""
x_ag=xagclass.Xag(1) #13,13  13-14;12-16
for i in range(13,14):#ma
    for j in range(13,14):#late
        xag, xagfag,CIrate=x_ag.ot(100000, 5, 1,j, x_ag.o, x_ag.c, x_ag.h, x_ag.l, x_ag.ts, x_ag.c1, i)
        tex = (i, j, 5,  len(xag) / 2, xag[-1][0], xagclass.getrate(xag),CIrate)
        print(tex)
        f.write(str(tex) + '\r')
#xagclass.writeee(xag)

"""

f.close()
