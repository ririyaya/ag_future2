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
# import talib
import csv
import codecs
import numpy as np
import matplotlib.pyplot as plt  # 重命名为plt
import datetime



class GetData(object):
    def __init__(self, d1, d2, table='ag15' ):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()
        sq = 'select (c-o)/o as oc_rate,(h-l)/o hl_rate from ' + table + ' where t between \''+str(d1)+'\' and \''+str(d2)+'\' order by ts'  # +' where ts>1635346800000'
        get_d='select t from (select distinct t,ts from '+ table + ' )t  order by ts'
        # print(sq)
        d.execute(sq)
        self.a = np.array(d.fetchall() )
        # d.execute(get_d)
        # self.d_list=d.fetchall()

class Getd(object):
    def __init__(self,table='ag15' ):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()
        sq = 'select o,c,h,l from ' + table + ' where t between str(d1) and str(d2) order by ts'  # +' where ts>1635346800000'
        get_d='select t from (select distinct t,ts from '+ table + ' )t  order by ts'
        d.execute(get_d)
        self.d_list=(d.fetchall())

def mean2(x):
    y = np.sum(x) / np.size(x)
    return y

def corr2(a, b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum())
    return r


data=GetData('2023-04-04','2023-04-10','xag1d_1')
d_list=Getd('xag1d_1')

list1=[]


for i in range (len(d_list.d_list)-4):
    a = data.a
    b = GetData(list(d_list.d_list[i])[0],list(d_list.d_list[i+3])[0],'xag1d_1').a
    d = corr2(a, b)
    print(i,d)
    if d>0.95 or d<-0.95:
        list1.append([i,d,list(d_list.d_list[i])[0]])

print(list1)



# print(np.array(data.a) )


# Array1 = [[1, 2, 3], [4, 5, 6]]
# Array2 = [[11, 25, 346], [734, 48, 49]]
# Mat1 = np.array(Array1)
# Mat2 = np.array(Array2)
# correlation = np.corrcoef(Mat1, Mat2)
# print("矩阵1=\n", Mat1)
# print("矩阵2=\n", Mat2)
# print("相关系数矩阵=\n", correlation)


