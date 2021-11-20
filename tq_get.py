from datetime import datetime
from contextlib import closing
from tqsdk import TqApi, TqAuth
from tqsdk.tools import DataDownloader

api = TqApi(auth=TqAuth("ririyeye2", "6824qwe"))
ag06=['16','17','18','19','20','21','22' ]

#0 tick 60 1min
# 分钟线数据     start_dt=datetime(2015, 1, 1, 12), end_dt=datetime(2021, 7, 1, 16), csv_file_name="ag2206.csv")
kd = DataDownloader(api, symbol_list="SHFE.ag2206", dur_sec=0,
                    start_dt=datetime(2015, 1, 1, 12), end_dt=datetime(2022, 7, 1, 16), csv_file_name="ag2206.csv")
# 盘口Tick数据
td = DataDownloader(api, symbol_list="SHFE.ag2112", dur_sec=60,
                    start_dt=datetime(2015, 1, 1), end_dt=datetime(2020, 11, 13), csv_file_name="ag2112.csv")
# 使用with closing机制确保下载完成后释放对应的资源

def get_tk(na):
    for i in na:
        print(i)



with closing(api):
    while not kd.is_finished() or not td.is_finished():
        api.wait_update()
        print("progress: kline: %.2f%% tick:%.2f%%" % (kd.get_progress(), td.get_progress()))