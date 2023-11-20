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
import plotly绘图

##https://blog.csdn.net/chenxy_bwave/article/details/121052541

class GetData(object):
    def __init__(self, sql, table='xag1d_1', data_base='koudai'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database=data_base,  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        data = mydb.cursor()
        sql = sql
        # print(sq)
        data.execute(sql)
        self.nparr = np.array(data.fetchall())
        # self.data = list(map(lambda x: x[0] , tmp))  #- tmp[0][0]


class Getd(object):
    def __init__(self, table='ag15'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        data = mydb.cursor()
        get_d = 'select  (from_unixtime(ts/1000)) from (select distinct t,ts from ' + table + ' where c<>o and h<>l and c<>h)t ' \
                  'order by ts'
        data.execute(get_d)
        self.d_list = (data.fetchall())


def dtw_distance(s1, s2):
    DTW = {}
    s1=list(map(lambda x: float(x), s1))
    s2=list(map(lambda x: float(x), s2))
    s1.reverse()
    s2.reverse()

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
    sql = 'select distinct  (c-o)/o from %s where ts=unix_timestamp(\'%s\')*1000' % (table, d_list[d_list.index(date1) + 1])
    # print(sq)
    data.execute(sql)
    return round(data.fetchall()[0][0], 4)*100


def data_len_compare(d_l1, d_l2):
    # date_l1 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l1[1], end=d_l1[2]))]
    # date_l2 = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=d_l2[1], end=d_l2[2]))]
    date_l1 = [x for x in d_list[d_list.index(d_l1[1]):d_list.index(d_l1[2]) + 1]]
    date_l2 = [x for x in d_list[d_list.index(d_l2[1]):d_list.index(d_l2[2]) + 1]]
    if len(set(date_l1) & set(date_l2)) >= len1 / 2:
        return 0
    else:
        return 1

if __name__ == '__main__':
    print(time.time(), '开始运行')

    d1 = '2023-09-01 15:00'
    d2 = '2023-09-02 04:00'
    ta = 'xag1h_ma20'
    sq = 'select dt,c,o,ma20,round((c-ma20)/ma20*100,3) from koudai.%s   order by ts  ' % ta

    plotly绘图.GetAndDraw(d1,d2,ta)

    all_data = GetData(sq, ta)
    d_list = list(map(lambda x: x[0], all_data.nparr))
    # d_list = list(map(lambda x: str(x[0]), Getd(ta).d_list))
    len1 = d_list.index(d2)-d_list.index(d1)
    unclean_dtw_list = [[0.0,d1,d2]]

    # print(all_data.nparr[d_list.index(d2)+1, 1])
    roll_data1 = all_data.nparr[d_list.index(d1):d_list.index(d2), 4].tolist()
    # 数据循环起点
    print(time.time(), '数据读取完成')
    for j in range(100, len(d_list) - 2 * len1):
        print(j)
        for i in range(len1 - 3, len1 + 2):
            if d_list[j + i+len1] == d_list[-1]:
                break
            else:
                roll_data2 = all_data.nparr[j+i:j+i+len1, 4].tolist()
                dtw_dist = dtw_distance(roll_data1, roll_data2)
                tmp_list=[dtw_dist,d_list[j+i],d_list[j+i+len1]]
                flag_lan_compare = data_len_compare(unclean_dtw_list[-1], tmp_list)
                if flag_lan_compare == 0 and unclean_dtw_list[-1][0]>dtw_dist:
                    unclean_dtw_list.pop()
                    unclean_dtw_list.append(tmp_list)
                elif flag_lan_compare == 1:
                    unclean_dtw_list.append(tmp_list)
                # else:
                    # print(lll)
                # unclean_dtw_list.sort()

    print(time.time(), 'dtw计算完成')

    result_list = sorted(unclean_dtw_list)[2:]
    next_d_ratio = []
    # d_list.index(result_list[i][2])
    for i in range(len(result_list)):
        o=all_data.nparr[d_list.index(result_list[i][2])+1, 2].tolist()
        c=all_data.nparr[d_list.index(result_list[i][2])+1, 1].tolist()
        result_list[i].append(round( (float(all_data.nparr[d_list.index(result_list[i][2]) +1, 1].tolist()) -float(all_data.nparr[d_list.index(result_list[i][2]) +1, 2].tolist()) )/ float(all_data.nparr[d_list.index(result_list[i][2])+1, 2].tolist())*100, 2))

        if result_list[i][0] <= 2:
            next_d_ratio.append(round( (float(all_data.nparr[d_list.index(result_list[i][2]) +1, 1].tolist()) -float(all_data.nparr[d_list.index(result_list[i][2]) +1, 2].tolist()) )/ float(all_data.nparr[d_list.index(result_list[i][2])+1, 2].tolist())*100, 2) )

    print(time.time(), '收益计算完成')
    print(result_list)

    dtw_ratio=0
    print(len(next_d_ratio))
    for i in range(len(next_d_ratio)):
        dtw_ratio+=next_d_ratio[i]
    dtw_avg_next_d = dtw_ratio / len(next_d_ratio)
    next_ratio = get_close_ratio(d2,ta)
    ratio_com = (d2, next_ratio, dtw_avg_next_d)
    print(ratio_com)

    for i in result_list:
        print(i[0])
        sql= "select c,ma20,dt from %s where dt between '%s' and '%s'" % (ta, i[1], i[2])
        plotly绘图.pltdraw(GetData(sql).nparr, i[1], i[2])

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
