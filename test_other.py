import numpy as np
import matplotlib.pyplot as plt
import threading
import yfinance as yf
import yfinance as yf2
import yfinance as yf3
import yfinance as yf4
import yfinance as yf5
import requests
import pandas as pd
import pickle
import time
from datetime import datetime
import datetime as dt
import json

# ----------------------字串測試-----------------------------
# a = 1
# b = 2
# c = f"a = {a}\nb = {b}"
# d = "1"
# e = c + d
# print(e)
# -------------------------時間+1以取得當天的數據------------------------------

TargetStockNoGroup = '3105.TWO'
end_date = dt.date.today() + dt.timedelta(days=1)
start_date = end_date - dt.timedelta(days=10)
print(end_date)
df_data = yf.download(TargetStockNoGroup, start=start_date, end=end_date)
print(df_data)
# if df_data.iloc[-1]['Close'] > df_data.iloc[-2]['Close'] : 
#     print( "a" )
# else:
#     print( "b" )
# print(df_data.iloc[-1]['Close'])
# print(df_data.iloc[-2]['Close'])
# print(df_data['Close'].tail(1))

# ----------------------------------------存成json----------------------

# def renew_data():
#     # filepath = "./Output.pkl"
#     # while os.path.isfile(filepath):
#     #     os.remove(r"./Input.pkl")
#     #     os.remove(r"./r_Input.pkl")
#     #     os.remove(r"./Output.pkl")
#     #     os.remove(r"./r_Output.pkl")
    
#     #上市資料
#     EFurl = 'https://www.twse.com.tw/fund/TWT38U?response=json&date=&_=1644690000895'
#     res = requests.get(EFurl)
#     data = res.json()
#     data_all = data['data']

#     df_all = []
#     for i in range (len(data_all)):
#         get0=[]
#         for j in range(1,3):
#             get0.append(data_all[i][j])
#         df_all.append(get0)

#         result = []
#     for i in range(len(df_all)):
#         result0=[]
#         for j in range(0,2):
#             result0.append(df_all[i][j].replace(" ",""))
#         result.append(result0)

#     df_all = result
#     df_LN= pd.DataFrame(df_all, columns=["ID", "Name"] )
#     df_LN['ID'] = df_LN['ID'].astype(str)
#     aL_InputNam = zip(df_LN['Name'], df_LN['ID']+".TW")
#     aL_InputNum = zip(df_LN['ID'], df_LN['ID']+".TW")
#     aL_Output = zip(df_LN['ID']+".TW", df_LN['Name'] + "("+ df_LN['ID']+")")

#     L_InputNam = dict(aL_InputNam)
#     L_InputNum = dict(aL_InputNum)
#     L_Output = dict(aL_Output)

#     ##上櫃資料

#     url = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&_=1659636941450'
#     res = requests.get(url)
#     data = res.json()
#     data_all = data['aaData']
#     df_all = []
#     for i in range (len(data_all)):
#         get0=[]
#         for j in range(0,2):
#             get0.append(data_all[i][j])
#         df_all.append(get0)

#         result = []
#     for i in range(len(df_all)):
#         result0=[]
#         for j in range(0,2):
#             result0.append(df_all[i][j].replace(" ",""))
#         result.append(result0)

#     df_all = result
#     df_ON= pd.DataFrame(df_all, columns=["ID", "Name"] )
#     df_ON['ID'] = df_ON['ID'].astype(str)
#     aO_InputNam = zip(df_ON['Name'],df_ON['ID']+".TWO")
#     aO_InputNum = zip(df_ON['ID'], df_ON['ID']+".TWO")
#     aO_Output = zip(df_ON['ID']+".TWO", df_ON['Name'] + "("+df_ON['ID']+")")

#     O_InputNam = dict(aO_InputNam)
#     O_InputNum = dict(aO_InputNum)
#     O_Output = dict(aO_Output)

#     #merge
#     ################
#     Input = {**L_InputNam, **L_InputNum, **O_InputNam, **O_InputNum}
#     a_file = open('Input.pkl', "wb")
#     pickle.dump(Input, a_file)
#     a_file.close()

#     Output = {**L_Output, **O_Output}

#     a_file = open('Output.pkl', "wb")
#     pickle.dump(Output, a_file)
#     a_file.close()
#     #################
#     #################
#      #上市資料
#     EFurl = 'https://www.twse.com.tw/fund/TWT38U?response=json&date=&_=1644690000895'
#     res = requests.get(EFurl)
#     data = res.json()
#     data_all = data['data']

#     df_all = []
#     for i in range (len(data_all)):
#         get0=[]
#         for j in range(1,3):
#             get0.append(data_all[i][j])
#         df_all.append(get0)

#         result = []
#     for i in range(len(df_all)):
#         result0=[]
#         for j in range(0,2):
#             result0.append(df_all[i][j].replace(" ",""))
#         result.append(result0)

#     df_all = result
#     df_LN= pd.DataFrame(df_all, columns=["ID", "Name"] )
#     df_LN['ID'] = df_LN['ID'].astype(str)
#     aL_InputNam = zip(df_LN['Name'], df_LN['ID'])
#     aL_InputNum = zip(df_LN['ID'], df_LN['ID'])
#     aL_Output = zip(df_LN['ID']+".TW", df_LN['Name'] + "("+ df_LN['ID']+")")

#     L_InputNam = dict(aL_InputNam)
#     L_InputNum = dict(aL_InputNum)
#     L_Output = dict(aL_Output)

#     ##上櫃資料

#     url = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&_=1659636941450'
#     res = requests.get(url)
#     data = res.json()
#     data_all = data['aaData']
#     df_all = []
#     for i in range (len(data_all)):
#         get0=[]
#         for j in range(0,2):
#             get0.append(data_all[i][j])
#         df_all.append(get0)

#         result = []
#     for i in range(len(df_all)):
#         result0=[]
#         for j in range(0,2):
#             result0.append(df_all[i][j].replace(" ",""))
#         result.append(result0)

#     df_all = result
#     df_ON= pd.DataFrame(df_all, columns=["ID", "Name"] )
#     df_ON['ID'] = df_ON['ID'].astype(str)
#     aO_InputNam = zip(df_ON['Name'],df_ON['ID'])
#     aO_InputNum = zip(df_ON['ID'], df_ON['ID'])
#     aO_Output = zip(df_ON['ID']+".TWO", df_ON['Name'] + "("+df_ON['ID']+")")

#     O_InputNam = dict(aO_InputNam)
#     O_InputNum = dict(aO_InputNum)
#     O_Output = dict(aO_Output)

#     #merge
#     ################
#     Input = {**L_InputNam, **L_InputNum, **O_InputNam, **O_InputNum}

#     Output = {**L_Output, **O_Output}
#     return Output

# A = renew_data()

# StockNumList = list(A.keys())
# StockNameList = list(A.values())

# for Num in StockNumList:
#     if len(Num.split('.')[0]) != 4:
#         del A[Num]

# with open("data.json", "w") as f:
    # json.dump(A, f)
# with open("data.json", "r") as f:
#     data = json.load(f)

# print(len(data))
# print(data)

# ----------------------------------------yf.download多股票----------------------
# num = 2
# tickers = ['1907.TW', '2330.TW']
# dfs = [pd.DataFrame() for _ in range(num)]
# end_date = dt.date.today()
# start_date = end_date - dt.timedelta(days=10)
# df_data = yf.download(tickers, start=start_date, end=end_date)

# for i in range(num):
#     df = df_data[tickers[i]]
#     # 计算2天内的最高价
#     df['2D_High'] = df['High'].rolling(window=2).max()
#     dfs[i] = df

# for df in dfs:
#     print(df)
#     print(df_data)
#     print("aaaaaaaa")

# tickers = ['1907.TW', '2330.TW', '2303.TW', '2603.TW', '8888.TW']
# # tickers = ['1907.TW', '2330.TW']
# num_tickers = len(tickers)
# end_date = dt.date.today()
# start_date = end_date - dt.timedelta(days=10)

# # 下载数据
# df_data = yf.download(tickers, start=start_date, end=end_date)
# # print(df_data)
# # 计算每个股票的两天内最高价
# for i in range(num_tickers):
#     df = pd.DataFrame()
#     df['Open'] = df_data['Open'][tickers[i]]
#     df['High'] = df_data['High'][tickers[i]]
#     df['Low'] = df_data['Low'][tickers[i]]
#     df['Close'] = df_data['Close'][tickers[i]]
#     df['Volume'] = df_data['Volume'][tickers[i]]

#     df['TwoDayHigh'] = df['Close'].rolling(window=2).max()
#     # df['TwoDayHigh'] = df['High'].rolling(window=2).max()
#     # 檢查每個元素是否為NaN
#     is_nan = df.isna()
#     # 檢查所有元素是否都是NaN
#     all_nan = is_nan.all().all()
#     if is_nan:
#         print( "fail" )
#         continue
#     else:
#         print("success")
#     print(df)

# ----------------------------------------計算距離早上9點幾分鐘----------------------
# now = datetime.now()
# nine_am = datetime(now.year, now.month, now.day, 9, 0, 0)

# if now < nine_am:
#     time_diff = nine_am - now
#     time_diff_minutes = time_diff.total_seconds() // 60
#     print(f"現在距離下一個早上九點還有 {time_diff_minutes} 分鐘")
# else:
#     next_day_nine_am = datetime(now.year, now.month, now.day+1, 9, 0, 0)
#     time_diff = now - nine_am
#     time_diff_minutes = time_diff.total_seconds() // 60
#     print(f"現在距離下一個早上九點已經過了 {time_diff_minutes} 分鐘")

# ----------------------------時間換算成成交量公式-------------------------------
# arr = list(range(271))
# y_list = []

# for minute in arr:
#     Time1 = 60
#     Volume1 = 0.7
#     Time2 = 180
#     Volume2 = 1.2
#     Final_Volune = 2
#     if minute >= 0 and minute <= Time1:
#         y = Volume1 * ( 1 - np.exp(-minute / 20) )
#     elif minute > Time1 and minute <= Time2:
#         y = Volume1 + ( Volume2 - Volume1 )/( Time2 - Time1 ) * ( minute - Time1 )
#     elif minute > Time2 and minute <= 270:
#         y = Volume2 + (Final_Volune - Volume2) * np.exp( (minute - 270) / 20 )
#     else:
#         y = 2
#     y_list.append(y)

# plt.plot(arr, y_list)
# plt.show()
