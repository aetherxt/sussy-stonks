import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pymongo
from datetime import datetime
import json 
import talib as ta
import math

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["stoccs"]
print("ok")

mycol = mydb["data"]

ticker = yf.download("MSFT", period = "2y")

ticker['RSI'] = ta.RSI(ticker['Close'], timeperiod=14)
ticker['MA10'] = ta.SMA(ticker['Close'], timeperiod=10)
ticker['MA20'] = ta.SMA(ticker['Close'], timeperiod=20)
ticker['MA50'] = ta.SMA(ticker['Close'], timeperiod=50)
ticker['MA100'] = ta.SMA(ticker['Close'], timeperiod=100)
ticker['MA200'] = ta.SMA(ticker['Close'], timeperiod=200)

tickerloc = -1
prevclose = 0
action = "S"
profit = 0
accumprofit = []
a = 0

def actionmsg():
    global prevclose, accumprofit
    profit = ticker['Close'][tickerloc] - prevclose
    accumprofit.append(profit)
    print(f"{list(ticker.index)[tickerloc]}: {round(ticker['Close'][tickerloc])}, {action}, {round(profit, 3)}")
    prevclose = round(ticker['Close'][tickerloc], 3)

for ma20 in ticker['MA20']:
    tickerloc += 1
    if not math.isnan(ma20):
        if (ma20 < ticker['MA50'][tickerloc] and ticker['MA10'][tickerloc] < ticker['MA50'][tickerloc]) or (ticker['RSI'][tickerloc] < 30):
            if action == "B":
                pass
            else: 
                action = "B"
                actionmsg()
        elif (ma20 > ticker['MA10'][tickerloc]) or (ticker['RSI'][tickerloc] > 70):
            if action == "S":
                pass
            else:
                action = "S"
                actionmsg()

accumprofit.pop(0)
for x in accumprofit:
    a += x

print(a)
