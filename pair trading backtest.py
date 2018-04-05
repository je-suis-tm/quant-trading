# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:57:46 2018

@author: Administrator
"""

#special thx to my mentor Giampiero Gallo and his mentor Robert Engle for their tremendous contributions to VCEM

#need to get fix yahoo finance package first
#also some basic understanding of time series and behavioral finance


#pair trading is also called mean reversion trading
#we find two cointegrated assets, normally a stock and an ETF index
#or two stocks in the same industry
#we run an cointegration test on the historical data
#we set the trigger condition for both stocks
#theoretically these two stocks cannot drift away from each other
#its like a drunk man with a dog
#the invisible dog leash would keep both assets in line
#when one stock is getting too bullish, we short the bullish one and long the bearish one, vice versa
#after several lags of time, the dog would converge to the drunk man
#its when we make profits
#nevertheless, the backtest is based on historical datasets
#in real stock market, market conditions are dynamic
#two assets may seem cointegrated for the past two years
#they just drift far away from each other after one company launch a new product or whatsoever
#i am talking about nvidia and amd, two gpu companies
#after nvidia launched neural network optimized gpu
#the stock price went skyrocketing
#amd didnt change much
#the cointegrated relationship just broke up
#so be extremely cautious with cointegration
#there is no such thing as riskless statistical arbitrage
#always check the cointegration status before trading execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.tsa.stattools as ta
import fix_yahoo_finance as yf

#the sample i am using are NVDA and AMD from 2012 to 2015
stdate=input('start date in format yyyy-mm-dd:')
eddate=input('end date in format yyyy-mm-dd:')
ticker1=input('ticker1:')
ticker2=input('ticker2:')
#slicing the downloaded dataset
#if the dataset is too large
#backtesting plot would look messy
st=int(input('slicing:'))


df1=yf.download(ticker1,start=stdate,end=eddate)
df2=yf.download(ticker2,start=stdate,end=eddate)


signals=pd.DataFrame()
signals['asset1']=df1['Close']
signals['asset2']=df2['Close']
#this is the part where we test the cointegration
#in this case, i use Engle-Granger two-step method, which is invented by the mentor of my mentor!!!
#generally people use Johanssen test to check the cointegration status
#the first step for EG is to run a linear regression on both variables
#we take the residual and run ADF test
#if it is stationary, we can determine its a drunk man with a dog
#the first step would be adding a constant vector to asset1
#next, we do OLS, we take asset2 as a regressor
#we printout the summary report to check the significance of coefficients
#we obtain the residual and run unit root test then
#if t value is statistical siginificant, we proceed to the next phrase
x=sm.add_constant(signals['asset1'])
y=signals['asset2']
model=sm.OLS(y,x).fit()
print(model.summary())
resid=model.resid
print('\n',ta.adfuller(resid))

#this phrase is how we set the trigger conditions
#first we normalize the residual so that we get a vector that follows standard normal distribution
#generally speaking, most tests use one sigma level as the threshold
#two sigma level reaches 95% which is relatively difficult to trigger
#after normalization, we should obtain a white noise follows N(0,1)
#we set +-1 as the threshold
#eventually we visualize the result
signals['z']=z=(resid-np.mean(resid))/np.std(resid)
#i use z*0 to get panda series instead of an integer result
signals['z upper limit']=z*0+np.mean(z)+np.std(z)
signals['z lower limit']=z*0+np.mean(z)-np.std(z)
fig1=plt.figure()
ax=fig1.add_subplot(211)
z.plot(label='z statistics')
signals['z upper limit'].plot(label='+1 sigma',linestyle=':')
signals['z lower limit'].plot(label='-1 sigma',linestyle=':')
plt.legend(loc='best')
plt.title('cointegration normalized residual')
plt.xlabel('time interval')
plt.show()


#the signal generation process is very straight forward
#if the normalized residual gets above or below threshold
#we long the bearish one and short the bullish one
#i only need to generate trading signal of one asset
#the other one should be the inverse
signals['signals1']=0
signals['signals1'][1:]=np.where(signals['z'][1:]>signals['z upper limit'][1:],1,0)
signals['signals1'][1:]=np.where(signals['z'][1:]>signals['z lower limit'][1:],1,0)
#signals only imply holding
#we take the first order difference to obtain the execution signal
signals['trade1']=signals['signals1'].diff()
signals['signals2']=-signals['signals1']
signals['trade2']=signals['signals2'].diff()
#the initial positions for both assets set to 1
#as i am an individual investor
#i cannot short any positions other than i long the position first
signals['trade1'][0]=signals['trade2'][0]=1


#next phrase is to visualize how i long/short both assets
new=signals[st:]
fig2=plt.figure()
bx=fig2.add_subplot(212)
new['asset1'].plot(label='asset 1')
new['asset2'].plot(label='asset 2')
bx.plot(new.loc[new['trade1']==1].index,new['asset1'][new['trade1']==1],lw=0,marker='^',label='long asset 1',c='g')
bx.plot(new.loc[new['trade1']==-1].index,new['asset1'][new['trade1']==-1],lw=0,marker='v',label='short asset 1',c='r')
bx.plot(new.loc[new['trade2']==1].index,new['asset2'][new['trade2']==1],lw=0,marker='^',label='long asset 2',c='g')
bx.plot(new.loc[new['trade2']==-1].index,new['asset2'][new['trade2']==-1],lw=0,marker='v',label='short asset 2',c='r')
bx.legend(loc='best')
plt.title('pair trading')
plt.xlabel('time interval')
plt.ylabel('price')
plt.show()


#how to calculate stats could be found from my other code called Heikin-Ashi
# https://github.com/tattooday/quant-trading/blob/master/heikin%20ashi%20backtest.py
