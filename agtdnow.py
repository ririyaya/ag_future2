import requests
import os
import re
import json
import time
import mysql.connector
import math
import numpy as np
import talib



def get(tm,count='25'):#type1,2,3,4,5:1m,5m,15m,30m,60m qid 6,agtd,13 xag
 url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=4&count="+str(count)+"&ts="+str(tm)
 header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
 r=requests.post(url,headers=header)
 candle=json.loads(r.text)['data']['candle']


 return candle

 def ma_o(li, candle, ma):
  o = int(candle[-1]['o'])
  mao = (o + sum(li[1:ma])) / ma
  return mao


ma = 13

count = 25
while True:
 tm = int(time.time() * 1000)
 candle = get(tm, count)
 li = []
 rate = []
 for i in range(0, len(candle)):
  li.append(float(candle[i]['c']))
 li.reverse()
 # print(li)
 for i in range(int(count) - ma):
  rate.append(round((sum(li[i:i + ma]) - sum(li[i + 1:i + 1 + ma])) / sum(li[i + 1:i + 1 + ma]) * 100000, 3))
 print(round(ma_o(li, candle, ma), 2), rate)
 time.sleep(60)