import Breakout
import GetData

# 更新股票清單
# GetData.GenListJson()

# 搜尋全部
print( Breakout.Breakout( 1, "" ) )


# 搜尋特定股票，因yfinance回傳格式，至少要兩隻
# print( Breakout.Breakout( 0, ['2412.TW', "2330.TW"]) )