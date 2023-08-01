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


class Dtw_data(object):
    def __init__(self, date1, date2, sql, table='xag1d', data_base='koudai'):  #
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database=data_base,  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')
        data = mydb.cursor()
        sql = sql % (table, date1, date2)
        # print(sq)
        data.execute(sql)
        tmp = np.array(data.fetchall())
        self.data = list(map(lambda x: x[0] - tmp[0][0], tmp))  # 起点归零
        self.len_d_range = len(self.data)


def Getd(ta='xag1d'):  # 日期列表
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="111",
        database='koudai',  # 数据库
        auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
    data = mydb.cursor()
    get_d = 'select t from (select distinct t,ts from ' + ta + ' where c<>o and h<>l and c<>h)t  order by ts'
    data.execute(get_d)
    return data.fetchall()


def dtw_distance(s1, s2):
    dtw = {}
    for i in range(len(s1)):
        dtw[(i, -1)] = float('inf')
    for i in range(len(s2)):
        dtw[(-1, i)] = float('inf')
    dtw[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i] - s2[j]) ** 2
            dtw[(i, j)] = dist + min(dtw[(i - 1, j)], dtw[(i, j - 1)], dtw[(i - 1, j - 1)])
    # print(dtw)
    return math.sqrt(dtw[len(s1) - 1, len(s2) - 1])


def get_close_ratio(date1, table='xag1d', data_base='koudai'):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="111",
        database=data_base,  # 数据库
        auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
    data = mydb.cursor()
    sql = 'select distinct (o-c)/c from %s where t=\'%s\'' % (table, d_list[d_list.index(date1) + 1])
    # print(sq)
    data.execute(sql)
    return data.fetchall()


def data_len_compare(d_l1, d_l2, len1):
    # date_l1 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l1[1], end=d_l1[2]))]
    # date_l2 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l2[1], end=d_l2[2]))]
    date_l1 = [x for x in d_list[d_list.index(d_l1[1]):d_list.index(d_l1[2]) + 1]]
    date_l2 = [x for x in d_list[d_list.index(d_l2[1]):d_list.index(d_l2[2]) + 1]]
    if len(set(date_l1) & set(date_l2)) >= len1 / 5:
        return False
    else:
        return True


table = 'xag1d'
ratio_com = []
# sq = 'select  round((c-o)/o*100,3) r2 from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
sq = 'select c from (select distinct o,c,h,l,t,ts,v from koudai.%s where c<>o and h<>l and c<>h)dis_t where t >=\'%s\' and t<=\'%s\' order by ts'
d_list = list(map(lambda x: x[0], Getd(table)))
# print(len(d_list))

for k in range(1350, len(d_list) - 19, 2):
    d1, d2 = d_list[k], d_list[k + 19]
    roll_data = Dtw_data(d1, d2, sq, table)
    len1 = roll_data.len_d_range

    unclean_dtw_list = []
    for i in range(1, len(d_list) - 2 * len1):
        for j in range(len1 - 5, len1 + 5):
            roll_data2 = Dtw_data((d_list[i]), (d_list[j + i]), sq, table)
            # roll_data3 = list(map(lambda x: x + (roll_data.data[0][0] - roll_data2.data[0][0]), roll_data2.data))
            if d_list[j + i] >= d1:
                break
            else:
                dtw_dist = dtw_distance(roll_data.data, roll_data2.data)
                unclean_dtw_list.append([dtw_dist, d_list[i], d_list[j + i]])

    unclean_dtw_list.sort()
    result_list = unclean_dtw_list

    for i in range(len(unclean_dtw_list)):
        if i >= len(result_list):
            break
        tmp_list = result_list[0:i + 1]
        for j in range(i, len(result_list)):
            if data_len_compare(result_list[i], result_list[j], len1) is True:
                tmp_list.append(result_list[j])

        result_list, tmp_list = tmp_list, []

    next_d_ratio = 0
    for i in range(len(result_list)):
        if result_list[i][0] <= 2:
            next_d_ratio += get_close_ratio(result_list[i][2])[0][0]

    dtw_avg_next_d = next_d_ratio / len(result_list)
    next_ratio = get_close_ratio(d2)
    ratio_com.append([d2, next_ratio, dtw_avg_next_d])
    print(k, ratio_com)

print(ratio_com)
