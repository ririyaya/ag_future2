import json
import math
import os
import re
import time
from decimal import Decimal as Dec
from decimal import getcontext
import mysql.connector
import requests
# import talib
import csv
import codecs
import numpy as np
import matplotlib.pyplot as plt  # 重命名为plt
import datetime
import pylab


class GetData(object):
    def __init__(self, date1, date2, sql, table='xag1d_1', data_base='koudai'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database=data_base,  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        data = mydb.cursor()
        # sq = 'select c from ' + table + ' where t between \''+str(d1)+'\' and \''+str(d2)+'\' order by ts'  # +' where ts>1635346800000'
        sql = sql % (table, date1, date2)
        # print(sq)
        data.execute(sql)
        self.a = np.array(data.fetchall())

class Getd(object):
    def __init__(self, table='ag15'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        data = mydb.cursor()
        # sq = 'select o,c from ' + table + ' where t between str(d1) and str(d2) order by ts'  # +' where ts>1635346800000'
        get_d = 'select t from (select distinct t,ts from ' + table + ' where c<>o and h<>l and c<>h)t  order by ts'
        data.execute(get_d)
        self.d_list = (data.fetchall())

def mean2(x):
    y = np.sum(x) / np.size(x)
    return y

def corr2(a, b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum())
    return r


list1 = []
d1 = '2023-06-05'
d2 = '2023-07-05'
ta = 'xag1d'
sq = 'select  round((c-o)/o*100,3) r2 from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
sq = 'select c from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
# sq = 'select c,ma20 from xag1h_ma20'

roll_data = GetData(d1, d2, sq, ta)
d_list = Getd(ta)
corr_rate = 0.95


try:
    for i in range(len(d_list.d_list) - len(roll_data.a)):
        a = roll_data.a
        b = GetData(list(d_list.d_list[i])[0], list(d_list.d_list[i + len(a) - 1])[0], sq, ta).a
        d = corr2(a, b)
        # print(i,d)
        if d > corr_rate:
            list1.append([i, d, list(d_list.d_list[i])[0], list(d_list.d_list[i + len(a) - 1])[0]])
            print(d, list(d_list.d_list[i])[0], list(d_list.d_list[i + len(a) - 1])[0])
except :
    print(list(d_list.d_list[i])[0], list(d_list.d_list[i + len(a) - 1])[0],)

print(len(roll_data.a), len(list1))

# Array1 = [[1, 2, 3], [4, 5, 6]]
# Array2 = [[11, 25, 346], [734, 48, 49]]
# Mat1 = np.array(Array1)
# Mat2 = np.array(Array2)
# correlation = np.corrcoef(Mat1, Mat2)
# print("矩阵1=\n", Mat1)
# print("矩阵2=\n", Mat2)
# print("相关系数矩阵=\n", correlation)

