import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
import talib

ma = 16           #13,16
def get(tm, count=25):  # type1,2,3,4,5:1m,5m,15m,30m,60m qid   6,agtd,    13 xag ,   704 fu
    urlxag = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=13&type=5&count=" + str(
        count) + "&ts=" + str(tm)
    url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=4&count=" + str(
        count) + "&ts=" + str(tm)
    header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
    if ma==13:
        r = requests.post(url, headers=header)
    elif ma==16:
        r = requests.post(urlxag, headers=header)
    else:print('请求方法error')
    candle = json.loads(r.text)['data']['candle']

    return candle


def ma_o(li, candle, ma):
    o = float(candle[-1]['o'])
    mao = (o + sum(li[1:ma])) / ma
    mac = sum(li[:ma])/ma
    return round(mao,2),round(mac,2)




count = 25
while True:
    tm = int(time.time() * 1000)
    candle = get(tm)
    li = []
    rate = []
    for i in range(0, len(candle)):
        li.append(float(candle[i]['c']))
    li.reverse()
    # print(li)
    for i in range(int(count) - ma):
        rate.append(round((sum(li[i:i + ma]) - sum(li[i + 1:i + 1 + ma])) / sum(li[i + 1:i + 1 + ma]) * 100000, 3))
    print(ma_o(li, candle, ma),'等第一个确定为信号', rate)
    #print(li)
    time.sleep(60)
