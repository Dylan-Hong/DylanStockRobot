import pandas as pd
import numpy as np
import yfinance as yf 
import datetime as dt
from datetime import datetime
import time
import json


class cParam():
    def __init__(self):
        # 需要設定的參數
        self.GetStockAmount = 100
        self.RefVolume = self.getVolumnRef()
        # 計算用的變數
        self.CountBreak = 0
        self.TargetNum = 0
        self.TargetStockNumList = []
        self.TargetStockNameList = []
        # 記錄執行時間
        self.start_time = time.time()
        # 設定時間
        self.end_date = dt.date.today() + dt.timedelta(days=1) # 因為yfinance只會抓end date的前一天，所以+1才變當天
        self.start_date = self.end_date - dt.timedelta(days=100)
        self.AccTime_yf = 0
        self.StartTime_yf = 0
        # 讀取股票清單
        self.StockNumList, self.StockNameList = self.LoadStockList()

    def getVolumnRef(self):
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

    def LoadStockList(self):
        with open("data.json", "r") as f:
            StockList_Dict = json.load(f)
        return list(StockList_Dict.keys()), list(StockList_Dict.values())

    def resetTargetList(self):
        # reset Target list相關參數
        self.TargetNum = 0
        self.TargetStockNumList = []
        self.TargetStockNameList = []

    def AddStockToTarget(self, index):
        # 把完整list的股票逐一塞到target內
        self.TargetStockNumList.append( self.StockNumList[index] )
        self.TargetStockNameList.append( self.StockNameList[index] )
        self.TargetNum += 1
        if len(self.TargetStockNumList) < self.GetStockAmount and index != (int( len( self.StockNumList ) ) - 1):
            return True
        else:
            return False

class cOutputData():
    def __init__(self):
        self.Found = []
        self.Fail_yf = []
        self.BreakoutList = []
        self.FirstBreakoutList = []
    def GetResult(self, AllParam : cParam):
        end_time = time.time()

        ResultStr = "輸出結果 : "
        ResultStrList = []
        ResultStrList.append(f"Breakout = {self.BreakoutList}")
        ResultStrList.append(f"FirstBreakout = {self.FirstBreakoutList}")
        ResultStrList.append(f"Fail_yf = {self.Fail_yf}")
        ResultStrList.append(f"CountBreak = {AllParam.CountBreak}")
        ResultStrList.append(f"Time = {(end_time - AllParam.start_time):.2f}秒, yf Time = {AllParam.AccTime_yf:.2f}秒")
        for str in ResultStrList:
            ResultStr = f"{ResultStr}\n{str}"
        return ResultStr

# 根據價量算出需要用的指標
def CalcIndicator( df: pd.DataFrame ):
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
def CalcCondition( df : pd.DataFrame, StockIndex, AllParam : cParam, OutputData : cOutputData ):

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
    Cond1 = Volume_RT > Volume_5MA * AllParam.RefVolume
    # 條件2 : 40日以來最高價
    Cond2 = Price_RT >= Price_High
    # 條件3 : 五日線/二十日線 < 1.02 -> 確保均線靠近
    Cond3 = Price_5MA / Price_20MA < 1.02
    # 條件4 : 二十日的布林帶寬最大值小於0.09
    Cond4 = BW_MaxIn20 < 0.09

    global CountBreak
    if Cond1 and Cond2:
        OutputData.BreakoutList.append(AllParam.TargetStockNameList[StockIndex])
        AllParam.CountBreak += 1
        if Cond3 and Cond4:
            OutputData.FirstBreakoutList.append(AllParam.TargetStockNameList[StockIndex])
    # print( "FailCondition = ", bin( Cond1 | Cond2 << 1 | Cond3 << 2 | Cond4 << 3 ) )

# 計算單一隻股票是否突破
def CalcOneStock( df_AllData : pd.DataFrame, AllParam : cParam, OutputData : cOutputData, StockIndex ):

    # 把當前要搜尋的股票放到df
    df = pd.DataFrame()
    df['Open'] = df_AllData['Open'][AllParam.TargetStockNumList[StockIndex]]
    df['High'] = df_AllData['High'][AllParam.TargetStockNumList[StockIndex]]
    df['Low'] = df_AllData['Low'][AllParam.TargetStockNumList[StockIndex]]
    df['Close'] = df_AllData['Close'][AllParam.TargetStockNumList[StockIndex]]
    df['Volume'] = df_AllData['Volume'][AllParam.TargetStockNumList[StockIndex]]

    # 檢查每個元素是否為NaN，代表下載資料失敗
    is_nan = df.isna()
    # 檢查所有元素是否都是NaN
    all_nan = is_nan.all().all()
    if all_nan:
        OutputData.Fail_yf.append(AllParam.TargetStockNameList[StockIndex])
        return
    else:
        OutputData.Found.append(AllParam.TargetStockNameList[StockIndex])

    CalcIndicator(df)
    CalcCondition(df, StockIndex, AllParam, OutputData)

def Breakout():
    AllParam = cParam()
    OutputData = cOutputData()

    # 搜尋特定股票，因yfinance回傳格式，至少要兩隻
    # AllParam.StockNumList = AllParam.StockNameList = ['6485.TWO', "3105.TWO"]

    # 搜尋所有股票
    for AllListIndex in range( 0, int( len( AllParam.StockNumList ) ) ):
        # 1. 把股票放進Target
        # 若還沒塞完跳過下面計算重新塞
        if AllParam.AddStockToTarget(AllListIndex):
            continue
        # 若已達到想要的數量，開始下載資料
        else:
            pass

        # 2. 一次撈一批歷史資料
        AllParam.StartTime_yf = time.time()
        df_data = yf.download(AllParam.TargetStockNumList, start=AllParam.start_date, end=AllParam.end_date)
        AllParam.AccTime_yf = time.time() - AllParam.StartTime_yf + AllParam.AccTime_yf

        # 3. 各自跑迴圈計算
        for StockIndex in range( 0, len(AllParam.TargetStockNumList) ) :
            CalcOneStock(df_data, AllParam, OutputData, StockIndex)

        # 清空Target
        AllParam.resetTargetList()

        # # 每掃600隻印一次出來
        # if AllListIndex % 600 == 599:
        #     print('Breakout = ', OutputData.BreakoutList)
        #     print('FirstBreakoutList = ', OutputData.FirstBreakoutList)

    return OutputData.GetResult(AllParam)