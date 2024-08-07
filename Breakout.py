import pandas as pd
import numpy as np
import yfinance as yf 
import datetime as dt
from datetime import datetime
import time
import json


class cParam():
    def __init__(self, SearchAllStock):
        # 需要設定的參數
        self.GetStockAmount = 100
        self.RefVolume = self.getVolumnRef()
        self.SearchAllStock = SearchAllStock
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
        self.KeepBreakoutList = []
        self.VCPBreakoutList = []
        self.RiseBreakoutList = []
    def GetResult(self, AllParam : cParam):
        end_time = time.time()
        now = dt.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S").split(".")[0]  # 取得秒之前的部分，去除秒的小數部分

        ResultStr = f"{current_time} 分析結果 : "
        ResultStrList = []
        ResultStrList.append(f"● 持續帶量創高 : \n{self.KeepBreakoutList}")
        ResultStrList.append(f"——————————")
        ResultStrList.append(f"● 壓縮後帶量突破 : \n{self.VCPBreakoutList}")
        ResultStrList.append(f"——————————")
        ResultStrList.append(f"● 上漲後突破 : \n{self.RiseBreakoutList}")
        ResultStrList.append(f"——————————")
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
    # 前40日最高價
    df['max_Price'] = df['High'].rolling(window=40).max()
    # 計算收盤價的20天標準差
    df["Close_std"] = df["Close"].rolling(window=20).std()
    # 布林帶寬
    df["BW"] = df["Close_std"] * 4.2 / df['MA_20']
    df['max_BWIn20'] = df['BW'].rolling(window=20).max()

# 判斷是否為突破
def CalcCondition( df : pd.DataFrame, StockIndex, AllParam : cParam, OutputData : cOutputData ):
    TargetName = AllParam.TargetStockNameList[StockIndex]
    # 若搜尋特定股票，因為沒給名稱所以代號當名字
    if AllParam.SearchAllStock == 0:
        TargetName = AllParam.TargetStockNumList[StockIndex]
    # 取出當天資料
    # 當下價格
    Price_RT = float(df.iloc[-1]['Close'])
    # 當下成交量
    Volume_RT = float(df.iloc[-1]['Volume']) # 單位為股

    # 給需要計算數值變數
    # 前一天的5日均量
    Volume_5MA = float(df.iloc[-2]['Vol_5ma'])
    # 前一天的40日最高價格
    Price_RecentHigh = float(df.iloc[-2]['max_Price'])
    # 前一天的5日均價
    Price_5MA = float(df.iloc[-2]['MA_5'])
    # 前一天的20日均價
    Price_20MA = float(df.iloc[-2]['MA_20'])
    # 前10天布林帶寬最大值
    BW_MaxIn20 = float(df.iloc[-2]['max_BWIn20'])
    # 前一天的最高
    Price_LastHigh = float(df.iloc[-2]['High'])

    Cond = [0] * 7
    Index = 0
    # 條件0 : 成交量出量
    Cond[Index] = Volume_RT > Volume_5MA * AllParam.RefVolume
    Index += 1
    # 條件1 : 40日以來最高價
    Cond[Index] = Price_RT > Price_RecentHigh
    Index += 1
    # 條件2 : 五日線/二十日線 < 1.02 -> 確保均線靠近
    Cond[Index] = Price_5MA / Price_20MA < 1.02
    Index += 1
    # 條件3 : 二十日的布林帶寬最大值小於0.09
    Cond[Index] = BW_MaxIn20 < 0.09
    Index += 1
    # 條件4 : 前一天有沒有創高
    Cond[Index] = not (Price_LastHigh == Price_RecentHigh)
    Index += 1
    # 條件5 : 五日均量超過300張
    Cond[Index] = Volume_5MA > 300000
    Index += 1
    # 條件6 : 當天均量超過500張
    Cond[Index] = Volume_RT > (500000 * AllParam.RefVolume)
    Index += 1

    global CountBreak
    if Cond[0] and Cond[1]:
        AllParam.CountBreak += 1
        # 壓縮後出量突破
        if Cond[2] and Cond[3] and Cond[6]:
            OutputData.VCPBreakoutList.append(TargetName)
        # 上漲後出量突破
        elif Cond[4] and Cond[5]:
            OutputData.RiseBreakoutList.append(TargetName)
        # 持續出量創高
        elif Cond[5]:
        # else:
            OutputData.KeepBreakoutList.append(TargetName)
        # else:
        #     print(f"{TargetName},{Volume_5MA},{Volume_RT}")

    # 若搜尋特定股票，印出沒找到的條件
    if AllParam.SearchAllStock == 0:
        Result = 0
        for i in range( 0, len(Cond) ):
            Result |= (Cond[i] << i)
        print( "FailCondition = ", bin( Result ) )
        print( df )

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

def Breakout(SearchAllStock, SpecificList):
    AllParam = cParam(SearchAllStock)
    OutputData = cOutputData()

    # 若要搜尋特定股票，替換掉整個list
    if SearchAllStock == 0:
        AllParam.StockNumList = SpecificList


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

