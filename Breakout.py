import os
import requests
import pandas as pd
import numpy as np
import pickle
import yfinance as yf 
import matplotlib.pyplot as plt
import talib
import math
import re
import requests
import datetime as dt
from datetime import datetime
import twstock
import time

# todo : mutli-thread
def renew_data():
    # filepath = "./Output.pkl"
    # while os.path.isfile(filepath):
    #     os.remove(r"./Input.pkl")
    #     os.remove(r"./r_Input.pkl")
    #     os.remove(r"./Output.pkl")
    #     os.remove(r"./r_Output.pkl")
    
    #上市資料
    EFurl = 'https://www.twse.com.tw/fund/TWT38U?response=json&date=&_=1644690000895'
    res = requests.get(EFurl)
    data = res.json()
    data_all = data['data']

    df_all = []
    for i in range (len(data_all)):
        get0=[]
        for j in range(1,3):
            get0.append(data_all[i][j])
        df_all.append(get0)

        result = []
    for i in range(len(df_all)):
        result0=[]
        for j in range(0,2):
            result0.append(df_all[i][j].replace(" ",""))
        result.append(result0)

    df_all = result
    df_LN= pd.DataFrame(df_all, columns=["ID", "Name"] )
    df_LN['ID'] = df_LN['ID'].astype(str)
    aL_InputNam = zip(df_LN['Name'], df_LN['ID']+".TW")
    aL_InputNum = zip(df_LN['ID'], df_LN['ID']+".TW")
    aL_Output = zip(df_LN['ID']+".TW", df_LN['Name'] + "("+ df_LN['ID']+")")

    L_InputNam = dict(aL_InputNam)
    L_InputNum = dict(aL_InputNum)
    L_Output = dict(aL_Output)

    ##上櫃資料

    url = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&_=1659636941450'
    res = requests.get(url)
    data = res.json()
    data_all = data['aaData']
    df_all = []
    for i in range (len(data_all)):
        get0=[]
        for j in range(0,2):
            get0.append(data_all[i][j])
        df_all.append(get0)

        result = []
    for i in range(len(df_all)):
        result0=[]
        for j in range(0,2):
            result0.append(df_all[i][j].replace(" ",""))
        result.append(result0)

    df_all = result
    df_ON= pd.DataFrame(df_all, columns=["ID", "Name"] )
    df_ON['ID'] = df_ON['ID'].astype(str)
    aO_InputNam = zip(df_ON['Name'],df_ON['ID']+".TWO")
    aO_InputNum = zip(df_ON['ID'], df_ON['ID']+".TWO")
    aO_Output = zip(df_ON['ID']+".TWO", df_ON['Name'] + "("+df_ON['ID']+")")

    O_InputNam = dict(aO_InputNam)
    O_InputNum = dict(aO_InputNum)
    O_Output = dict(aO_Output)

    #merge
    ################
    Input = {**L_InputNam, **L_InputNum, **O_InputNam, **O_InputNum}
    a_file = open('Input.pkl', "wb")
    pickle.dump(Input, a_file)
    a_file.close()

    Output = {**L_Output, **O_Output}

    a_file = open('Output.pkl', "wb")
    pickle.dump(Output, a_file)
    a_file.close()
    #################
    #################
     #上市資料
    EFurl = 'https://www.twse.com.tw/fund/TWT38U?response=json&date=&_=1644690000895'
    res = requests.get(EFurl)
    data = res.json()
    data_all = data['data']

    df_all = []
    for i in range (len(data_all)):
        get0=[]
        for j in range(1,3):
            get0.append(data_all[i][j])
        df_all.append(get0)

        result = []
    for i in range(len(df_all)):
        result0=[]
        for j in range(0,2):
            result0.append(df_all[i][j].replace(" ",""))
        result.append(result0)

    df_all = result
    df_LN= pd.DataFrame(df_all, columns=["ID", "Name"] )
    df_LN['ID'] = df_LN['ID'].astype(str)
    aL_InputNam = zip(df_LN['Name'], df_LN['ID'])
    aL_InputNum = zip(df_LN['ID'], df_LN['ID'])
    aL_Output = zip(df_LN['ID']+".TW", df_LN['Name'] + "("+ df_LN['ID']+")")

    L_InputNam = dict(aL_InputNam)
    L_InputNum = dict(aL_InputNum)
    L_Output = dict(aL_Output)

    ##上櫃資料

    url = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&_=1659636941450'
    res = requests.get(url)
    data = res.json()
    data_all = data['aaData']
    df_all = []
    for i in range (len(data_all)):
        get0=[]
        for j in range(0,2):
            get0.append(data_all[i][j])
        df_all.append(get0)

        result = []
    for i in range(len(df_all)):
        result0=[]
        for j in range(0,2):
            result0.append(df_all[i][j].replace(" ",""))
        result.append(result0)

    df_all = result
    df_ON= pd.DataFrame(df_all, columns=["ID", "Name"] )
    df_ON['ID'] = df_ON['ID'].astype(str)
    aO_InputNam = zip(df_ON['Name'],df_ON['ID'])
    aO_InputNum = zip(df_ON['ID'], df_ON['ID'])
    aO_Output = zip(df_ON['ID']+".TWO", df_ON['Name'] + "("+df_ON['ID']+")")

    O_InputNam = dict(aO_InputNam)
    O_InputNum = dict(aO_InputNum)
    O_Output = dict(aO_Output)

    #merge
    ################
    Input = {**L_InputNam, **L_InputNum, **O_InputNam, **O_InputNum}

    Output = {**L_Output, **O_Output}
    return Output

def getVolumnRef():
    now = datetime.now()
    nine_am = datetime(now.year, now.month, now.day, 9, 0, 0)

    # 若時間為開盤後
    if now > nine_am:
        time_diff = now - nine_am
        time_diff_minutes = time_diff.total_seconds() // 60
    #若時間為開盤前
    else:
        time_diff_minutes = 270 # 未開盤因為沒當天資料，因此當作收盤了

    # 設定開盤區間與收盤前時間跟比例
    Time1 = 60
    Volume1 = 0.7
    Time2 = 180
    Volume2 = 1.2
    Final_Volune = 2
    if time_diff_minutes >= 0 and time_diff_minutes <= Time1:
        RefVolume = Volume1 * ( 1 - np.exp(-time_diff_minutes / 20) )
    elif time_diff_minutes > Time1 and time_diff_minutes <= Time2:
        RefVolume = Volume1 + ( Volume2 - Volume1 )/( Time2 - Time1 ) * ( time_diff_minutes - Time1 )
    elif time_diff_minutes > Time2 and time_diff_minutes <= 270:
        RefVolume = Volume2 + (Final_Volune - Volume2) * np.exp( (time_diff_minutes - 270) / 20 )
    else:
        RefVolume = 2
    return RefVolume

Found = []
Fail_yf = []
Fail_Realtime = []
BreakoutList = []
FirstBreakoutList = []

def Breakout():
    start_time = time.time()
    CountAll = 0
    CountBreak = 0
    CountNotBreak = 0
    CountNoVol = 0
    CountStock = 0
    A = renew_data()
    StockNumList = list(A.keys())
    StockNameList = list(A.values())
    # 設定時間
    end_date = dt.date.today()
    start_date = end_date - dt.timedelta(days=100)
    # 搜尋特定股票
    # StockNumList = ['3114.TWO']

    # 搜尋所有股票
    for StockIndex in range( 0, int(len( StockNumList )) ):
        TargetStockNo = StockNumList[StockIndex]
        TargetStockName = StockNameList[StockIndex]
        CountAll += 1
        # 跳過ETF跟權證
        if len(TargetStockNo.split('.')[0]) != 4 :
            continue
        else:
            CountStock += 1

        # 1.撈即時資料
        try:
            # 建立一個股票物件
            stock = yf.Ticker(TargetStockNo) # xxxx.TW

            # 獲取即時股價和成交量資料
            stock_Realtime = stock.history(period="1d")

            # 給需要計算數值變數
            # 當下價格
            Price_RT = float(stock_Realtime['Close'][0])
            # 當下成交量
            Volume_RT = float(stock_Realtime['Volume'][0]) # 單位為股

        except (ValueError, KeyError, IndexError, TypeError) as e:
            # 如果讀取失敗，輸出錯誤訊息
            print("讀取資料失敗: ", e)
            Fail_Realtime.append(TargetStockName)
            continue

        # 初步篩選：篩選最低成交量，10點前 < 140張，收盤前 < 400張，直接跳過
        if CountAll % 100 == 1:
            RefVolume = getVolumnRef()
        if Volume_RT < RefVolume * 200 * 1000:
            CountNoVol += 1
            continue

        # 2.撈歷史資料

        # download會回傳dataframe的資料
        print(TargetStockNo)
        df_data = yf.download(TargetStockNo, start=start_date, end=end_date)
        # 若yfinance找不到，跳過
        if df_data.empty:
            Fail_yf.append(TargetStockName)
            continue
        else:
            Found.append(TargetStockName)
        # 計算均值獲最大值
        # 用talib畫出均線
        df_data[ 'MA_5' ] = talib.SMA(np.array(df_data['Close']), 5)
        df_data[ 'MA_20' ] = talib.SMA(np.array(df_data['Close']), 20)
        df_data[ 'Vol_5ma'] = df_data['Volume'].rolling(5).mean()
        df_data['max_Price'] = df_data['High'].rolling(window=40).max()
        # 計算收盤價的20天標準差
        df_data["Close_std"] = df_data["Close"].rolling(window=20).std()
        # 布林帶寬
        df_data["BW"] = df_data["Close_std"] * 4.2 / df_data['MA_20']
        df_data['max_BWIn20'] = df_data['BW'].rolling(window=20).max()

        # 給需要計算數值變數
        # 5日均量
        Volume_5MA = float(df_data['Vol_5ma'].tail(1))
        # 近日最高價格
        Price_High = float(df_data['max_Price'].tail(1))
        # 5日均價
        Price_5MA = float(df_data['MA_5'].tail(1))
        # 20日均價
        Price_20MA = float(df_data['MA_20'].tail(1))
        # 前10天布林帶寬最大值
        BW_MaxIn20 = float(df_data['max_BWIn20'].tail(1))


        # 條件1 : 成交量出量
        Cond1 = Volume_RT > Volume_5MA * RefVolume
        # 條件2 : 40日以來最高價
        Cond2 = Price_RT > Price_High
        # 條件3 : 五日線/二十日線 < 1.02 -> 確保均線靠近
        Cond3 = Price_5MA / Price_20MA < 1.02
        # 條件4 : 二十日的布林帶寬最大值小於0.09
        Cond4 = BW_MaxIn20 < 0.09

        if Cond1 and Cond2:
            BreakoutList.append(TargetStockName)
            CountBreak += 1
            if Cond3 and Cond4:
                FirstBreakoutList.append(TargetStockName)
        else:
            CountNotBreak += 1
        # print( "FailCondition = ", bin( Cond1 | Cond2 << 1 | Cond3 << 2 | Cond4 << 3 | Cond5 << 3 ) )

        # 每掃100隻印一次出來
        if CountAll % 100 == 0:
            print('Breakout = ', BreakoutList)
            print('FirstBreakoutList = ', FirstBreakoutList)

    print('Breakout = ', BreakoutList)
    print('FirstBreakoutList = ', FirstBreakoutList)
    print("Fail_yf = ", Fail_yf)
    print("Fail_Fail_Realtime = ", Fail_Realtime)
    print("CountBreak = ", CountBreak, ", CountNotBreak = ", CountNotBreak, "CountStock = ", CountStock , "CountNoVol = ", CountNoVol, "CountAll = ", CountAll)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"程式執行時間為 {elapsed_time:.2f} 秒")

Breakout()