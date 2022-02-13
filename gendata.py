import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pymongo
from datetime import datetime
import json 
import talib as ta

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["stoccs"]
print("ok")

mycol = mydb["data"]
now = datetime.now()
tickerlist = ["AAPL", "MSFT", "FB", "0700.hk"]

def newdata():
    mycol.drop({})
    for tickername in tickerlist:
        ticker = yf.download(tickername, period = "1y")
        ticker['SMA10'] = ta.SMA(ticker['Close'], timeperiod=10)
        ticker['SMA20'] = ta.SMA(ticker['Close'], timeperiod=20)
        ticker['SMA50'] = ta.SMA(ticker['Close'], timeperiod=50)
        if not ticker.empty:
            df = pd.DataFrame(ticker)
            data = df.reset_index()
            json_data = json.loads(data.to_json(date_format="iso"))
            data_list = []
            for j in range(len((json_data["Date"]))):
                row = {}
                for col in data.columns:
                    row[col] = json_data[col][str(j)]
                    if col == "Date":
                        row[col] = datetime.strptime(json_data[col][str(j)], '%Y-%m-%dT%H:%M:%S.%fZ')
                data_list.append(row)
            
            ticker_data = []
            for row in data_list:
                ticker_data.append(row)
                
            mycol.insert_one({tickername: ticker_data})

newdata()