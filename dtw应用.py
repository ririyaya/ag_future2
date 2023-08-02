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
import pandas as pd
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
        tmp = np.array(data.fetchall())
        self.data = list(map(lambda x: x[0] - tmp[0][0], tmp))


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


def get_close_ratio(date1, table='xag1d', data_base='koudai'):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="111",
        database=data_base,  # 数据库
        auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
    data = mydb.cursor()
    sql = 'select distinct  (c-o)/o from %s where t=\'%s\'' % (table, d_list[d_list.index(date1) + 1])
    # print(sq)
    data.execute(sql)
    return data.fetchall()


def data_len_compare(d_l1, d_l2):
    # date_l1 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l1[1], end=d_l1[2]))]
    # date_l2 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l2[1], end=d_l2[2]))]
    date_l1 = [x for x in d_list[d_list.index(d_l1[1]):d_list.index(d_l1[2]) + 1]]
    date_l2 = [x for x in d_list[d_list.index(d_l2[1]):d_list.index(d_l2[2]) + 1]]
    if len(set(date_l1) & set(date_l2)) >= len1 / 5:
        return False
    else:
        return True


d1 = '2023-06-19'
d2 = '2023-08-01'
ta = 'xag_1d_v_ratio'
# sq = 'select  round((c-o)/o*100,3) r2 from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
sq = 'select c from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'

# d_list = Getd(ta).d_list
d_list = list(map(lambda x: x[0], Getd(ta).d_list))
roll_data = GetData(d1, d2, sq, ta)
len1 = len(roll_data.data)
unclean_dtw_list = []

for j in range(1, len(d_list) - 2 * len1):
    print(j)
    for i in range(len1 - 5, len1 + 5):
        roll_data2 = GetData((d_list[j]), (d_list[j + i]), sq, ta)
        # roll_data3 = list(map(lambda x: x + (roll_data.data[0][0] - roll_data2.data[0][0]), roll_data2.data))
        if d_list[j + i] == d1:
            break
        else:
            dtw_dist = dtw_distance(roll_data.data, roll_data2.data)
            unclean_dtw_list.append([dtw_dist, d_list[j], d_list[j + i]])

unclean_dtw_list.sort()
tmp_list = []
result_list = unclean_dtw_list

for i in range(len(unclean_dtw_list)):
    # print(i)
    if i >= len(result_list):
        break
    # print(l4)
    tmp_list = result_list[0:i + 1]
    for j in range(i, len(result_list)):
        if data_len_compare(result_list[i], result_list[j]) is True:
            tmp_list.append(result_list[j])
            # print(i,j)
    result_list, tmp_list = tmp_list, []

print(result_list)

next_d_ratio = []
for i in range(len(result_list)):
    if result_list[i][0] <= 2:
        next_d_ratio.append(get_close_ratio(result_list[i][2])[0][0])

dtw_ratio=0
print(len(next_d_ratio))
for i in range(len(next_d_ratio)):
    dtw_ratio+=next_d_ratio[i]
dtw_avg_next_d = dtw_ratio / len(next_d_ratio)
next_ratio = get_close_ratio(d2)[0][0]
ratio_com= (d2, round(next_ratio, 4)*100, round(dtw_avg_next_d, 4)*100)
print(ratio_com)

# if os.path.exists(r"d:\2.txt"):
#     os.remove(r"d:\2.txt")
# f = open(r"d:\2.txt", "a", encoding='utf-8')
# f.write('%s\n\n' % l2)
# for i in range(len(l3)):
#     # if l5[i][0]<50:
#     print(i)
#     f.write('%s,%s,%s\n' % (i, l3[i], get_close_ratio(l3[i][2])[0][0]))
#
# # f.write(str(l4) + '\n')
# f.close()
# print(list(map(lambda x: x[2],  l5 )))
