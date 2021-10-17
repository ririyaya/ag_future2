import xagclass #整数特化ver,期货14,12,6(14,8-12,5-9)

import os
if os.path.exists(r"C:\Users\食蜂\Desktop\2.txt"):
    os.remove(r"C:\Users\食蜂\Desktop\2.txt")
f = open(r"C:\Users\食蜂\Desktop\2.txt", "a", encoding='utf-8')
a=xagclass.GetXag(1,'ag30')
for i in range(14,15):
    for j in range(12,13):
        for k in range(6,7,1):
            ee, log=a.ot(100000, k, j,a.o,a.c,a.h,a.l,a.ts,a.c1,i)
            tex=(i,j,k,len(ee) / 2, ee[-1][0],a.getrate(ee))
            #a.writeee(ee)
            print(tex)
            #print(ee[-2])
            f.write(str(tex)+'\r')

f.close()