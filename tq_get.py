from datetime import datetime
from contextlib import closing
from tqsdk import TqApi, TqAuth
from tqsdk.tools import DataDownloader

api = TqApi(auth=TqAuth("ririyeye2", "6824qwe"))
ag06=['16','17','18','19','20','21','22' ]

#0 tick 60 1min
"""
./mysql --local-infile=1 -uroot -p 
set global local_infile = 1;
create table tick_2206 (detm datetime,datetime_nano char(32),last_price int,highest int,lowest int,volume int,amount int,open_interest int,bid_price1 int,bid_volume1 int,ask_price1 int,ask_volume1 int);
mysql> LOAD DATA LOCAL INFILE '/home/erik/Documents/out10-2.csv'
INTO TABLE out10
FIELDS TERMINATED BY ','
IGNORE 1 LINES
"""

# 分钟线数据     start_dt=datetime(2015, 1, 1, 12), end_dt=datetime(2021, 7, 1, 16), csv_file_name="ag2206.csv")
kd = DataDownloader(api, symbol_list="SHFE.ag2206", dur_sec=0,
                    start_dt=datetime(2015, 1, 1, 12), end_dt=datetime(2020, 7, 1, 16), csv_file_name="ag22060.csv")
# 盘口Tick数据
td = DataDownloader(api, symbol_list="SHFE.ag2106", dur_sec=0,
                    start_dt=datetime(2020, 11, 1), end_dt=datetime(2021, 6, 30), csv_file_name="ag2106tick.csv")
# 使用with closing机制确保下载完成后释放对应的资源

def get_tk(na):
    for i in na:
        print(i)



with closing(api):
    while not kd.is_finished() or not td.is_finished():
        api.wait_update()
        print("progress: kline: %.2f%% tick:%.2f%%" % (kd.get_progress(), td.get_progress()))