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
        sql = sql % (table, date1, date2)
        # print(sq)
        data.execute(sql)
        self.data = np.array(data.fetchall())


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


def dtw_distance(s1, s2):
    DTW = {}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i] - s2[j]) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])
    # print(DTW)
    return math.sqrt(DTW[len(s1) - 1, len(s2) - 1])


list1 = []
d1 = '2023-06-05'
d2 = '2023-07-05'
ta = 'xag1d'
# sq = 'select  round((c-o)/o*100,3) r2 from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
sq = 'select c from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'


d_list = Getd(ta).d_list
roll_data = GetData(d1, d2, sq, ta)
len1 = len(roll_data.data)

l1, l2 = [], []
print(len(d_list) - len1, math.floor(len1 / 2), math.floor(len1 / 2))
# try:
for j in range(1000, len(d_list) - 2*len1):
    # for i in range(math.floor(len1 / 2), len1 + math.floor(len1 / 2)):
    for i in range(len1-5, len1+5):
        roll_data2 = GetData(list(d_list[j])[0], list(d_list[j + i])[0], sq, ta)
        roll_data3 = list(map(lambda x: x + (roll_data.data[0][0]-roll_data2.data[0][0]), roll_data2.data))
        # print(d_list[j + i][0],d1,d2)
        if d_list[j + i][0] == d1:
            # print(roll_data.data,roll_data2.data)
            break
        else:
            dtw_dist = dtw_distance(roll_data.data, roll_data2.data)
            # print(d_list[j], d_list[j+i], dtw_dist)
            # l1.append( d_list[j+i])
            l2.append([dtw_dist,d_list[j], d_list[j+i]])
            print(j)
# except :
#     print('err')

# print(sorted(l1)[-1:])

print(sorted(l2)[:10])


