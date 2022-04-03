import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
import json 
import talib as ta
import math

ticker = yf.download("2800.hk", period = "1y")

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
buyprice = 0

def actionmsg():
    global prevclose, accumprofit
    if action == "B":
        profit = 0
    else:
        profit = ticker['Close'][tickerloc] - prevclose
    accumprofit.append(profit)
    print(f"{list(ticker.index)[tickerloc]}: {round(ticker['Close'][tickerloc])}, {action}, {round(profit, 3)}")
    prevclose = round(ticker['Close'][tickerloc], 3)

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

print(a)
print(masell())