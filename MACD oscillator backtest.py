# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:57:46 2018

@author: Administrator
"""

#need to get fix yahoo finance package first
import os
os.chdir('D:/')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf
""""""
#input the long moving average and short moving average period
#for the classic MACD, it is 12 and 26
#once a upon a time you got six trading days in a week
#so it is two week moving average versus one month moving average
#for now, the ideal choice would be 10 and 21
ma1=int(input('ma1:'))
ma2=int(input('ma2:'))

stdate=input('start date in format yyyy-mm-dd:')
eddate=input('end date in format yyyy-mm-dd:')
ticker=input('ticker:')
#slicing the downloaded dataset
#if the dataset is too large, backtesting plot would look messy
#you get too many markers cluster together
st=int(input('slicing:'))


#downloading data and calculating moving average
df=yf.download(ticker,start=stdate,end=eddate)
signals=pd.DataFrame(df)
signals['ma1']=signals['Close'].rolling(window=ma1,min_periods=1,center=False).mean()
signals['ma2']=signals['Close'].rolling(window=ma2,min_periods=1,center=False).mean()

#signal generation
#when the short moving average is larger than long moving average, we long and hold
#when the short moving average is smaller than long moving average, we clear positions
#the logic behind this is that the momentum has more impact on short moving average
#we can subtract short moving average from long moving average
#the difference between is sometimes positive, it sometimes becomes negative
#thats why it is named as moving average converge/diverge oscillator

signals['signals']=0
#signal becomes and stays one once the short moving average is above long moving average
signals['signals'][ma1:]=np.where(signals['ma1'][ma1:]>=signals['ma2'][ma1:],1,0)
#as signals only imply the holding
#we take the difference to generate real trade signal
signals['trade']=signals['signals'].diff()
#take the slicing
new=signals[st:]

#plotting the backtesting result
#the first plot is the actual close price with long/short positions
#the second plot is long/short moving average oscillator
fig=plt.figure()
ax=fig.add_subplot(211)
new['Close'].plot(label='price')
ax.plot(new.loc[new['trade']==1].index,new['Close'][new['trade']==1],lw=0,marker='^',c='g')
ax.plot(new.loc[new['trade']==-1].index,new['Close'][new['trade']==-1],lw=0,marker='v',c='r')
plt.legend(loc='best')
plt.grid(True)

bx=fig.add_subplot(212)
new['ma1'].plot(label='ma1')
new['ma2'].plot(label='ma2',linestyle=':')
plt.legend(loc='best')
plt.grid(True)


plt.show()
#how to calculate stats could be found from my other code called Heikin-Ashi: https://github.com/tattooday/quant-trading/blob/master/heikin%20ashi%20backtest.py

