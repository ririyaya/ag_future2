import xagclass #整数特化ver,期货14,12,6(14,8-12,5-9)

import os
if os.path.exists(r"C:\Users\食蜂\Desktop\2.txt"):
    os.remove(r"C:\Users\食蜂\Desktop\2.txt")
f = open(r"C:\Users\食蜂\Desktop\2.txt", "a", encoding='utf-8')
f_ag=xagclass.GetXag(1, 'ag30')
for i in range(14,15):
    for j in range(12,13):
        for k in range(6,7,1):
            fag, log=f_ag.ot(100000, k, j, f_ag.o, f_ag.c, f_ag.h, f_ag.l, f_ag.ts, f_ag.c1, i)
            tex=(i, j, k, len(fag) / 2, fag[-1][0], f_ag.getrate(fag))
            #a.writeee(fag)
            print(tex)
            #print(fag[-2])
            #f.write(str(tex)+'\r')

f.close()

x_ag=xagclass.Xag(1)
xag,log=x_ag.ot(100000, 5, 15, x_ag.o, x_ag.c, x_ag.h, x_ag.l, x_ag.ts, x_ag.c1, 16)
tex = (16, 15, 5,  len(xag) / 2, xag[-1][0], x_ag.getrate(xag))
print(tex)