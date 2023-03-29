import os
import requests
import pandas as pd
import numpy as np
import pickle
import yfinance as yf 
import matplotlib.pyplot as plt
import math
import re
import requests
import datetime as dt
from datetime import datetime
import twstock
import time
import json

def LoadStockList():
    with open("data.json", "r") as f:
        StockList_Dict = json.load(f)
    return list(StockList_Dict.keys()), list(StockList_Dict.values())

# 根據價量算出需要用的指標
def CalcIndicator( df: pd.DataFrame, StockIndex ):
    # 計算均值 or 最大值
    df[ 'MA_5' ] = df['Close'].rolling(5).mean()
    df[ 'MA_20' ] = df['Close'].rolling(20).mean()
    df[ 'Vol_5ma'] = df['Volume'].rolling(5).mean()
    df['max_Price'] = df['High'].rolling(window=40).max()
    # 計算收盤價的20天標準差
    df["Close_std"] = df["Close"].rolling(window=20).std()
    # 布林帶寬
    df["BW"] = df["Close_std"] * 4.2 / df['MA_20']
    df['max_BWIn20'] = df['BW'].rolling(window=20).max()

# 判斷是否為突破
def CalcCondition( df : pd.DataFrame, StockIndex, TargetStockNameList : list ):

    # 取出當天資料
    # 當下價格
    Price_RT = float(df.iloc[-1]['Close'])
    # 當下成交量
    Volume_RT = float(df.iloc[-1]['Volume']) # 單位為股

    # 給需要計算數值變數
    # 5日均量
    Volume_5MA = float(df.iloc[-2]['Vol_5ma'])
    # 近日最高價格
    Price_High = float(df.iloc[-2]['max_Price'])
    # 5日均價
    Price_5MA = float(df.iloc[-2]['MA_5'])
    # 20日均價
    Price_20MA = float(df.iloc[-2]['MA_20'])
    # 前10天布林帶寬最大值
    BW_MaxIn20 = float(df.iloc[-2]['max_BWIn20'])

    # 條件1 : 成交量出量
    Cond1 = Volume_RT > Volume_5MA * RefVolume
    # 條件2 : 40日以來最高價
    Cond2 = Price_RT >= Price_High
    # 條件3 : 五日線/二十日線 < 1.02 -> 確保均線靠近
    Cond3 = Price_5MA / Price_20MA < 1.02
    # 條件4 : 二十日的布林帶寬最大值小於0.09
    Cond4 = BW_MaxIn20 < 0.09

    global CountBreak
    if Cond1 and Cond2:
        BreakoutList.append(TargetStockNameList[StockIndex])
        CountBreak += 1
        if Cond3 and Cond4:
            FirstBreakoutList.append(TargetStockNameList[StockIndex])
    # print( "FailCondition = ", bin( Cond1 | Cond2 << 1 | Cond3 << 2 | Cond4 << 3 ) )

# 計算單一隻股票是否突破
def CalcOneStock( df_AllData : pd.DataFrame, TargetStockNumList : list, TargetStockNameList : list, StockIndex ):
    # 把當前要搜尋的股票放到df
    df = pd.DataFrame()
    df['Open'] = df_AllData['Open'][TargetStockNumList[StockIndex]]
    df['High'] = df_AllData['High'][TargetStockNumList[StockIndex]]
    df['Low'] = df_AllData['Low'][TargetStockNumList[StockIndex]]
    df['Close'] = df_AllData['Close'][TargetStockNumList[StockIndex]]
    df['Volume'] = df_AllData['Volume'][TargetStockNumList[StockIndex]]

    # 檢查每個元素是否為NaN，代表下載資料失敗
    is_nan = df.isna()
    # 檢查所有元素是否都是NaN
    all_nan = is_nan.all().all()
    if all_nan:
        Fail_yf.append(TargetStockNameList[StockIndex])
        return
    else:
        Found.append(TargetStockNameList[StockIndex])

    CalcIndicator(df, StockIndex)
    CalcCondition(df, StockIndex, TargetStockNameList)

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

GetStockAmount = 100
Found = []
Fail_yf = []
BreakoutList = []
FirstBreakoutList = []
CountBreak = 0
RefVolume = getVolumnRef()

def Breakout():
    # 記錄執行時間
    start_time = time.time()
    # 讀取股票清單
    StockNumList, StockNameList = LoadStockList()
    # 設定時間
    end_date = dt.date.today() + dt.timedelta(days=1) # 因為yfinance只會抓end date的前一天，所以+1才變當天
    start_date = end_date - dt.timedelta(days=100)
    AccTime_yf = 0
    StartTime_yf = 0
    # 搜尋特定股票，因yfinance回傳格式，至少要兩隻
    # StockNumList = StockNameList = ['6485.TWO', "3105.TWO"]

    TargetNum = 0
    TargetStockNumList = []
    TargetStockNameList = []
    # 搜尋所有股票
    for AllListIndex in range( 0, int( len( StockNumList ) ) ):
        # 把完整list的股票逐一塞到target內
        TargetStockNumList.append( StockNumList[AllListIndex] )
        TargetStockNameList.append( StockNameList[AllListIndex] )
        TargetNum += 1

        # 把TargetList塞到想要的數量或是整個list跑完了，才繼續做後面的計算
        if len(TargetStockNumList) < GetStockAmount and AllListIndex != (int( len( StockNumList ) ) - 1):
            continue
        else:
            pass

        # 2.撈歷史資料
        # 一次撈一批歷史資料
        StartTime_yf = time.time()
        df_data = yf.download(TargetStockNumList, start=start_date, end=end_date)
        AccTime_yf = time.time() - StartTime_yf + AccTime_yf
        # 各自跑迴圈計算
        for StockIndex in range( 0, len(TargetStockNumList) ) :
            CalcOneStock(df_data, TargetStockNumList, TargetStockNameList, StockIndex)

        # reset Target list相關參數
        TargetNum = 0
        TargetStockNumList = []
        TargetStockNameList = []

        # 每掃600隻印一次出來
        if AllListIndex % 600 == 599:
            print('Breakout = ', BreakoutList)
            print('FirstBreakoutList = ', FirstBreakoutList)

    print('Breakout = ', BreakoutList)
    print('FirstBreakout = ', FirstBreakoutList)
    print("Fail_yf = ", Fail_yf)
    print("CountBreak = ", CountBreak)
    end_time = time.time()
    print(f"程式執行時間為 {(end_time - start_time):.2f} 秒", f"yf執行時間為 {AccTime_yf:.2f} 秒")

Breakout()