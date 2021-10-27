import xagclass #整数特化ver,期货14,12,6(14,8-12,5-9)

import os
'''
fag30,12,15,6
fag15,30,17,5
xag   16,15,5
'''

if os.path.exists(r"d:\2.txt"):
    os.remove(r"d:\2.txt")
f = open(r"d:\2.txt", "a", encoding='utf-8')
f_ag=xagclass.GetXag(1, 'ag30')
for i in range(12,13):#ma
    for j in range(15,16):#late
        for k in range(5,6,1):#xie
            for l in range(2,3):#startlate
                fag, log=f_ag.ot(100000, k, 2,j, f_ag.o, f_ag.c, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1, i)
                tex=(i, l,j, k, len(fag) / 2, fag[-1][0], xagclass.getrate(fag))
                xagclass.writeee(fag)
                print(tex)
                print(fag[-1])
                f.write(str(tex)+'\r')




'''
x_ag=xagclass.Xag(1) #13,13  13-14;12-16
for i in range(13,14):#ma
    for j in range(13,14):#late
        xag, xagfag,CIrate=x_ag.ot(100000, 5, 1,j, x_ag.o, x_ag.c, x_ag.h, x_ag.l, x_ag.ts, x_ag.c1, i)
        tex = (i, j, 5,  len(xag) / 2, xag[-1][0], xagclass.getrate(xag),CIrate)
        print(tex)
        f.write(str(tex) + '\r')
#xagclass.writeee(xag)

现货  时间  信号  状态
    
期货

'''
f.close()