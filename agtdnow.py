import requests
import os
import re
import json
import time
import smtp_mail
# import mysql.connector
import math


# import numpy as np
# import talib
def get(tm, count=25):  # type1,2,3,4,5:1m,5m,15m,30m,60m qid   6,agtd,    13 xag ,   704 fu
    urlxag = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=13&type=5&count=" + str(
        count) + "&ts=" + str(tm)
    url = "https://official.gkoudai.com/officialNetworkApi/CandleStickV2?qid=704&type=4&count=" + str(
        count) + "&ts=" + str(tm)
    header = {'epid': 'a6c89023-9472-4f30-81cf-8c7dea62aae5'}
    if ma == 13:
        r = requests.post(url, headers=header)
    elif ma == 20:
        r = requests.post(urlxag, headers=header)
    else:
        print('请求方法error')
    data_list = json.loads(r.text)['data']['candle']
    return data_list


def ma_o(li, candle, ma):
    o = float(candle[-1]['o'])
    ma_o = (o + sum(li[1:ma])) / ma
    ma_c = sum(li[:ma]) / ma
    return round(ma_o, 2), round(ma_c, 2)


ma = 20
count = 25
send_mail = smtp_mail.SendSmtpMail()

while True:
    tm = int(time.time() * 1000)
    candle = get(tm)
    close_list = []
    rate = []
    for i in range(0, len(candle)):
        close_list.append(float(candle[i]['c']))
    close_list.reverse()
    # print(li)
    for i in range(int(count) - ma):
        rate.append(round((sum(close_list[i:i + ma]) - sum(close_list[i + 1:i + 1 + ma])) / sum(close_list[i + 1:i + 1 + ma]) * 100000, 3))
    print(ma_o(close_list, candle, ma), '等第一个确定为信号', rate)
    #当前k开盘在ma上，若low在ma下，发送邮件
    ma_o_price = ma_o(close_list, candle, ma)[0]
    candle_now = candle[-1]
    del candle_now['a']
    del candle_now['t']
    del candle_now['ts']
    if float(candle[-1]['o']) > ma_o_price and float(candle[-1]['c']) <= (ma_o_price*0.99) :
        send_mail.mail(str(time.strftime("%Y-%m-%d %H:%M:%S"))+"\n"+str(candle_now)+"\n"+str(ma_o_price),"多头机会")
    elif float(candle[-1]['o'] )< ma_o_price and float(candle[-1]['c']) >= (ma_o_price*1.01) :
        send_mail.mail(str(time.strftime("%Y-%m-%d %H:%M:%S"))+"\n"+str(candle_now)+"\n"+str(ma_o_price),"空头机会")
    # print(li)
    time.sleep(600)


# {'a': '0.0', 'c': '23.1550', 't': '11-15 12:00', 'v': '3314.0', 'h': '23.2300', 'l': '23.1225', 'o': '23.1475', 'ts': 1700020800000}
