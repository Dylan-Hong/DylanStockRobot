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

def GenListJson():
    AllList = renew_data()

    StockNumList = list(AllList.keys())

    for Num in StockNumList:
        if len(Num.split('.')[0]) != 4:
            del AllList[Num]

    with open("data.json", "w") as f:
        json.dump(AllList, f)
    with open("data.json", "r") as f:
        data = json.load(f)

    print(data)

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

GetStockAmount = 10
Found = []
Fail_yf = []
Fail_Realtime = []
BreakoutList = []
FirstBreakoutList = []
Price_RT = [0] * GetStockAmount
Volume_RT = [0] * GetStockAmount
ErrorIndex = [0] * GetStockAmount # 若整批讀取的過程有錯誤，on起來標注那個錯誤

def Breakout():
    start_time = time.time()
    CountAll = 0
    CountBreak = 0
    CountNotBreak = 0
    CountNoVol = 0
    CountStock = 0 # 代表總共搜尋了多少股票
    TargetNum = 0 # 代表當前這個Target list裡面有多少股票
    ErrorIndex = [0] * GetStockAmount

    # 讀取股票清單
    StockNumList, StockNameList = LoadStockList()
    RefVolume = getVolumnRef()
    # 設定時間
    end_date = dt.date.today() + dt.timedelta(days=1) # 因為yfinance只會抓end date的前一天
    start_date = end_date - dt.timedelta(days=100)
    yftimeAll = 0
    yftimestart = 0
    yfrealtimeAll = 0
    yfrealtimestart = 0
    # 搜尋特定股票
    # StockNumList = ['1907.TW']

    TargetStockNumList = []
    TargetStockNameList = []
    # 搜尋所有股票
    for AllListIndex in range( 0, int( len( StockNumList )/80 ) ):

        # 跳過權證跟etf，這邊用代號是不是4碼來簡單判斷
        if len(StockNumList[AllListIndex].split('.')[0]) != 4 :
            continue
        # 若是有效的股票，塞進去TargetStockNumList裡面
        else:
            TargetStockNumList.append( StockNumList[AllListIndex] )
            TargetStockNameList.append( StockNameList[AllListIndex] )
            TargetNum += 1
            CountStock += 1

            # 把TargetList塞到想要的數量或是整個list跑完了，才繼續做後面的計算
            if len(TargetStockNumList) < GetStockAmount and AllListIndex != (int( len( StockNumList ) ) - 1):
                continue
            else:
                pass

        # 處理當天資料
        # for StockIndex in range( 0, len(TargetStockNumList) ):
        #     CountAll += 1

        #     # 1.撈即時資料
        #     try:
        #         yfrealtimestart = time.time()
        #         # 建立一個股票物件
        #         stock = yf.Ticker(TargetStockNumList[StockIndex]) # xxxx.TW

        #         # 獲取即時股價和成交量資料
        #         stock_Realtime = stock.history(period="1d")
        #         yfrealtimeAll = time.time() - yfrealtimestart + yfrealtimeAll

        #         # 給需要計算數值變數
        #         # 當下價格
        #         Price_RT[StockIndex] = float(stock_Realtime['Close'][0])
        #         # 當下成交量
        #         Volume_RT[StockIndex] = float(stock_Realtime['Volume'][0]) # 單位為股

        #     except (ValueError, KeyError, IndexError, TypeError) as e:
        #         # 如果讀取失敗，輸出錯誤訊息
        #         print("讀取資料失敗: ", e)
        #         Fail_Realtime.append(TargetStockName)
        #         ErrorIndex[StockIndex] = 1
        #         continue

        # # 初步篩選：篩選最低成交量，10點前 < 140張，收盤前 < 400張，直接跳過
        # if CountAll % 100 == 1:
        #     RefVolume = getVolumnRef()
        # if Volume_RT < RefVolume * 200 * 1000:
        #     CountNoVol += 1
        #     continue

        # 2.撈歷史資料
        # 一次撈一批歷史資料
        yftimestart = time.time()
        df_data = yf.download(TargetStockNumList, start=start_date, end=end_date)
        yftimeAll = time.time() - yftimestart + yftimeAll
        # 各自跑迴圈計算
        for StockIndex in range( 0, len(TargetStockNumList) ) :
            # 若real time就判斷失敗，跳過
            if ErrorIndex[StockIndex] == 1: 
                continue

            # 把當前要搜尋的股票放到df
            df = pd.DataFrame()
            df['Open'] = df_data['Open'][TargetStockNumList[StockIndex]]
            df['High'] = df_data['High'][TargetStockNumList[StockIndex]]
            df['Low'] = df_data['Low'][TargetStockNumList[StockIndex]]
            df['Close'] = df_data['Close'][TargetStockNumList[StockIndex]]
            df['Volume'] = df_data['Volume'][TargetStockNumList[StockIndex]]

            # print(TargetStockNumList[StockIndex])

            # 取出當天資料
            # 當下價格
            Price_RT[StockIndex] = float(df.iloc[-1]['Close'])
            # 當下成交量
            Volume_RT[StockIndex] = float(df.iloc[-1]['Volume']) # 單位為股

            # 檢查每個元素是否為NaN
            is_nan = df.isna()
            # 檢查所有元素是否都是NaN
            all_nan = is_nan.all().all()
            if all_nan:
                Fail_yf.append(TargetStockNameList[StockIndex])
                continue
            else:
                Found.append(TargetStockNameList[StockIndex])

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
            Cond1 = Volume_RT[StockIndex] > Volume_5MA * RefVolume
            # 條件2 : 40日以來最高價
            Cond2 = Price_RT[StockIndex] >= Price_High
            # 條件3 : 五日線/二十日線 < 1.02 -> 確保均線靠近
            Cond3 = Price_5MA / Price_20MA < 1.02
            # 條件4 : 二十日的布林帶寬最大值小於0.09
            Cond4 = BW_MaxIn20 < 0.09

            if Cond1 and Cond2:
                BreakoutList.append(TargetStockNameList[StockIndex])
                CountBreak += 1
                if Cond3 and Cond4:
                    FirstBreakoutList.append(TargetStockNameList[StockIndex])
            else:
                CountNotBreak += 1
            # print( "FailCondition = ", bin( Cond1 | Cond2 << 1 | Cond3 << 2 | Cond4 << 3 ) )

        # reset Target list相關參數
        TargetNum = 0
        TargetStockNumList = []
        TargetStockNameList = []

        # 每掃400隻印一次出來
        if CountAll % 400 == 5:
            print('Breakout = ', BreakoutList)
            print('FirstBreakoutList = ', FirstBreakoutList)

    print('Breakout = ', BreakoutList)
    print('FirstBreakoutList = ', FirstBreakoutList)
    print("Fail_yf = ", Fail_yf)
    print("Fail_Realtime = ", Fail_Realtime)
    print("CountBreak = ", CountBreak, ", CountNotBreak = ", CountNotBreak, "CountStock = ", CountStock , "CountNoVol = ", CountNoVol, "CountAll = ", CountAll)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"程式執行時間為 {elapsed_time:.2f} 秒", f"yf執行時間為 {yftimeAll:.2f} 秒", f"realtime執行時間為 {yfrealtimeAll:.2f} 秒")


# GenListJson()
Breakout()