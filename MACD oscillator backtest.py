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
#long moving average and short moving average
ma1=int(input('ma1:'))
ma2=int(input('ma2:'))

stdate=input('start date in format yyyy-mm-dd:')
eddate=input('end date in format yyyy-mm-dd:')
ticker=input('ticker:')
#slicing the downloaded dataset, if the dataset is too large, backtesting plot would look messy
st=int(input('slicing:'))


#downloading data and calculating moving average
df=yf.download(ticker,start=stdate,end=eddate)
signals=pd.DataFrame(df)
signals['ma1']=signals['Close'].rolling(window=ma1,min_periods=1,center=False).mean()
signals['ma2']=signals['Close'].rolling(window=ma2,min_periods=1,center=False).mean()

#signal generation, when the short moving average is larger than long moving average, we long and hold, otherwise we short

signals['signals']=0
signals['signals'][ma1:]=np.where(signals['ma1'][ma1:]>=signals['ma2'][ma1:],1,0)
#take the difference to generate trade signal
signals['trade']=signals['signals'].diff()
#take the slicing
new=signals[st:]

#plotting the backtesting result, the first plot is the actual price with long/short positions, the second plot is long/short moving average oscillator
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

