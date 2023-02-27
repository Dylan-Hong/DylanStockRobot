# DylanStockRobot


## 安裝TA-Lib 指南
在package中talib 沒辦法直接由pip install 安裝以下是安裝talib 步驟:
```
mkdir /opt/software
cd /opt/software
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -axvf ta-lib-0.4.0-src.tar.gz
cd /opt/softwar/ta-lib
./configure --prefix=/usr
make 
make install
pip install TA-Lib
```
執行過程中有遇到下列問題，提供解決方案：
* 如果在make 時遇到configure: error: no acceptable C compiler found in $PATH，則需要先安裝C編譯器

```
sudo yum -y install gcc
```

* 若出現 fatal error: Python.h 需額外執行下列 \

Ubuntu
```
sudo apt-get install python3-dev
```
Linux
```
sudo yum install python3-devel
```
# 更新紀錄
* 2023/2/27 新增FLASK設定以及README.md 對於安裝TA-lib的說明
