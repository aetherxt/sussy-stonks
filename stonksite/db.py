import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
import json
import talib as ta
import math
# import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["stoccs"]
# print("ok")

# mycol = mydb["data"]

def getticker(tickers, tickerperiod):
    ticker = yf.download(tickers, period = tickerperiod)

    ticker['RSI'] = ta.RSI(ticker['Close'], timeperiod=14)
    ticker['MA10'] = ta.SMA(ticker['Close'], timeperiod=10)
    ticker['MA20'] = ta.SMA(ticker['Close'], timeperiod=20)
    ticker['MA50'] = ta.SMA(ticker['Close'], timeperiod=50)
    ticker['MA100'] = ta.SMA(ticker['Close'], timeperiod=100)
    ticker['MA200'] = ta.SMA(ticker['Close'], timeperiod=200)
    
    return ticker

def estimate(ticker):
    tickerloc = -1
    prevclose = 0
    action = "S"
    profit = 0
    accumprofit = []
    a = 0
    buyprice = 0
    
    datelist, closelist, actionlist, profitlist = [], [], [], []

    def actionmsg():
        nonlocal prevclose, accumprofit, datelist, closelist, actionlist, profitlist
        profit = ticker['Close'][tickerloc] - prevclose
        accumprofit.append(profit)
        datelist.append(list(ticker.index)[tickerloc])
        closelist.append(ticker['Close'][tickerloc])
        actionlist.append(action)
        profitlist.append(profit)
        prevclose = (ticker['Close'][tickerloc])

    def getchange():
        return ((ticker['Close'][tickerloc-3] - ticker['Close'][tickerloc]) / ticker['Close'][tickerloc-3]) * 100.0

    def percentincrease():
        return ((buyprice - ticker['Close'][tickerloc]) / ticker['Close'][tickerloc]) * 100.0

    def mabuy():
        return ticker['MA20'][tickerloc] < ticker['MA50'][tickerloc] and ticker['MA10'][tickerloc] < ticker['MA50'][tickerloc]

    def masell():
        return getchange() >= 5 and (ticker['MA10'][tickerloc] > ticker['MA50'][tickerloc]) and percentincrease() >= 15

    def rsibuy():
        return ticker['RSI'][tickerloc] <= 40 

    def rsisell():
        return ticker['RSI'][tickerloc] >= 70

    for ma20 in ticker['MA20']:
        tickerloc += 1
        if not math.isnan(ma20):
            if (mabuy()) or (rsibuy()):
                if action == "B":
                    pass
                else: 
                    action = "B"
                    buyprice = ticker['Close'][tickerloc]
                    actionmsg()
            elif (masell()) or (rsisell()):
                if action == "S":
                    pass
                else:
                    action = "S"
                    actionmsg()

    accumprofit.pop(0)
    for x in accumprofit:
        a += x
    
    return datelist, closelist, actionlist, profitlist, a

def gengraph(ticker):
    magraph = ticker[['Close','MA10', 'MA20', 'MA50', 'MA100', 'MA200']].plot(figsize=(15, 10))
    rsigraph = ticker[['RSI']].plot(figsize=(15, 10))

