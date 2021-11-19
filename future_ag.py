import time
import trend  # 整数特化ver,期货14,12,6(14,8-12,5-9)
from updatedb import CONNECTSQL
import os

'''
fag30,13,25,5 #震荡18,10,6 爆亏 利润-0.3,胜率0.18
fag15,30,17,5
xag   16,15,5
'''


con_sql = CONNECTSQL('ag30', 4, 114)
#con_sql.updatedb(con_sql.mydb)
# con_sql.updatetxt()

if os.path.exists(r"d:\2.txt"):
    os.remove(r"d:\2.txt")
f = open(r"d:\2.txt", "a", encoding='utf-8')
# m1=xagclass.MIN1(15)
f_ag = trend.f_mod(1, 'ag30')  # 杠杆倍率,表,强制循环起点
for ma_range in range(6, 7):
    for maxlate in range(25, 26):
        for slope in range(5, 6):  # 斜率?
            for minlate in range(1, 2):  # startlate
                fag, log, CIrate = f_ag.ot(100000, slope, ma_range, minlate, maxlate, f_ag.o, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1)
                # fag, log, CIrate = f_ag.ot(100000, k, 2, j, m1.o, m1.h, m1.l, m1.ts, m1.c, i)
                tex = (ma_range, minlate, maxlate, slope, len(fag) / 2, fag[-1][0], trend.getrate(fag), round(CIrate, 3))
                print(tex)
                '''
                print(fag[-2])
                print(fag[-1])
                print('等收线')
                print(log[-1])'''
                #f.write(str(tex) + '\r')


title = '[总盈亏, 平仓盈亏, 开平方向, 开平点位, ma, o, c, h, l,time, 循环次数, 开仓延迟, 持仓,平仓利润率, 复利利润率, 最大浮盈, 最大浮亏, 持仓k数, 开仓延迟]'

exetend=[]
for i in range(1,len(fag)):
    if fag[i][2] in ['空平','多平']:
        exetend.append(fag[i]+[fag[i][10]-fag[i-1][10]]+[fag[i-1][11]])

trend.w_csv(exetend, '报表扩展')
trend.w_csv(fag, '报表')

try:
    time.sleep(1)
except Exception as e:
    print(e)
f.close()
