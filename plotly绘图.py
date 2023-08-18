import matplotlib.pyplot as plt
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

# import plotly.plotly as ply
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class GetData(object):
    def __init__(self,table='xag1h_ma1_ratio', data_base='koudai'):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database=data_base,  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        data = mydb.cursor()
        sql = 'select c,row_nber,series_count,series,ts,dt,series_ratio,ratio from %s ' \
              'where row_nber between 23000 and 25000 ' % (table)
        # print(sq)
        data.execute(sql)
        self.tmp = np.array(data.fetchall())
        # self.data = list(map(lambda x: x[0], self.tmp))

print(time.time())
da = GetData()
# length1=list(range(len(da.tmp)))
fig = make_subplots(specs=[[{"secondary_y": True}]])
# fig = go.Figure()
# Add traces
fig.add_trace(go.Scatter(x=da.tmp[:, 1], y=da.tmp[:, 0], mode='lines', name='c'),secondary_y=False)
fig.add_trace(go.Scatter(x=da.tmp[:, 1], y=da.tmp[:, 2], mode='lines', name='series', fill="tozeroy", xaxis='x', yaxis='y2'),secondary_y=True)
fig.add_trace(go.Bar(x=da.tmp[:, 1], y=da.tmp[:, 6], name='ratio', xaxis='x', yaxis='y2',marker={"color":'black',"opacity":1}),secondary_y=True)
fig.show()

# trace1 = go.Scatter(x=da.tmp[:, 1], y=da.tmp[:, 0], mode='lines', name='c')
# trace2 = go.Scatter(x=da.tmp[:, 1], y=da.tmp[:, 2], mode='lines', name='series', fill="tozeroy", xaxis='x', yaxis='y2')
# trace3 = go.Scatter(x=da.tmp[:, 1], y=da.tmp[:, 6], mode='lines', name='ratio', xaxis='x', yaxis='y2')
#
# data = [trace1, trace2]
# layout = go.Layout(
#     yaxis2=dict(anchor='x', overlaying='y', side='right')  # 设置坐标轴的格式，一般次坐标轴在右侧
# )
#
# fig = go.Figure(data=data, layout=layout)
# ply.iplot(fig)
