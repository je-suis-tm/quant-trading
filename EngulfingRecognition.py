'''Spotting candlestick chart pattern collectively for all stocks automatically. Formulas coded manually.'''

import csv
import numpy
from itertools import zip_longest

gravestone=[]
dateeee=[]
bearishengulf=[]
dateee=[]
bullishengulf=[]
datee=[]

def is_bullish_candlestick(candle):
    return float(candle['Close']>candle['Open'])

def is_bearish_candlestick(candle):
    return float(candle['Close']<candle['Open'])

def is_bullish_engulfing(candles,index):
    current_day=candles[index]
    previous_day=candles[index-1]
    
    if is_bearish_candlestick(previous_day) \
        and float(current_day['High'])>float(previous_day['Close']) \
        and float(current_day['Close'])>float(previous_day['Open']) \
        and float(current_day['Open'])<float(previous_day['Close']):
        return True

    return False

def is_bearish_engulfing(candles,index):
    current_day=candles[index]
    previous_day=candles[index-1]
    
    if is_bullish_candlestick(previous_day) \
        and float(current_day['Close'])<float(previous_day['Low'])\
        and float(current_day['Open'])>float(previous_day['High']):
        return True

    return False

def is_gravestone_doji(candles,index):
    current_day=candles[index]
    previous_day=candles[index-1]

    if is_bullish_candlestick(previous_day) \
        and float(current_day['High'])>float(previous_day['High'])\
        and float(current_day['Open'])>float(previous_day['Close'])\
        and float(current_day['Open'])==float(current_day['Low']) \
        and float(current_day['Close'])<=float(current_day['Open']):
        return True

    return False

def pattern_recognition_initializer(candles,index):
    current_day=candles[index]

    open=current_day['Open']
    high=current_day['High']
    low=current_day['Low']
    close=current_day['Close']

    open=numpy.array(open,dtype=float)
    high=numpy.array(high,dtype=float)
    low=numpy.array(low,dtype=float)
    close=numpy.array(close,dtype=float)
    

def pattern_recognition():
    symbols_file=open("Prerequisites-Outputs\Tickers.csv")
    tickers=csv.reader(symbols_file)

    for company in tickers:
        #print(company)

        ticker=company[0]

        history_file=open("Auto generated Dataset\{}.csv".format(ticker))

        reader=csv.DictReader(history_file)
        candles=list(reader)

        candles=candles[-2:]

        if len(candles)>1:
            if is_bullish_engulfing(candles,1):
                print("{} = {} is bullish engulfing".format(ticker,candles[1]['Date']))
                print("------------------------------------------------")
                bullishengulf.append("{}".format(ticker))
                datee.append("{}".format(candles[1]['Date']))

            if is_bearish_engulfing(candles,1):
                print("{} = {} is bearish engulfing".format(ticker,candles[1]['Date']))
                print("------------------------------------------------")
                bearishengulf.append("{}".format(ticker))
                dateee.append("{}".format(candles[1]['Date']))

            if is_gravestone_doji(candles,1):
                print("{} = {} is gravestone doji".format(ticker,candles[1]['Date']))
                print("------------------------------------------------")
                gravestone.append("{}".format(ticker))
                dateeee.append("{}".format(candles[1]['Date']))

            pattern_recognition_initializer(candles,1)
        
    list_clubber=[bullishengulf,datee]
    export_data_complete=zip_longest(*list_clubber,fillvalue='')

    with open("Prerequisites-Outputs\BullishEngulfing.csv",'w',encoding="ISO-8859-1",newline="") as myfile:
        wr=csv.writer(myfile)
        wr.writerow(("Ticker","Date Of Formation"))
        wr.writerows(export_data_complete)

    list_clubberr=[bearishengulf,dateee]
    export_data_completee=zip_longest(*list_clubberr,fillvalue='')

    with open("Prerequisites-Outputs\BearishEngulfing.csv",'w',encoding="ISO-8859-1",newline="") as myfile:
        wr=csv.writer(myfile)
        wr.writerow(("Ticker","Date Of Formation"))
        wr.writerows(export_data_completee)

    list_clubberrr=[gravestone,dateeee]
    export_data_completeee=zip_longest(*list_clubberrr,fillvalue='')

    with open("Prerequisites-Outputs\Gravestone.csv",'w',encoding="ISO-8859-1",newline="") as myfile:
        wr=csv.writer(myfile)
        wr.writerow(("Ticker","Date Of Formation"))
        wr.writerows(export_data_completeee)