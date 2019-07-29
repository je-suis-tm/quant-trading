# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:57:46 2018

@author: Administrator
"""

#special thx to my mentor Prof Giampiero M Gallo, 
#now a governor in Italy (neither League nor Five Star Movement)
#and his mentor Robert Engle, the nobel prize winner!
#for their tremendous contributions to VECM

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
#after bitcoin mining boom and machine learning hype
#stock price of nvidia went skyrocketing
#amd didnt change much on the contrary
#the cointegrated relationship just broke up
#so be extremely cautious with cointegration
#there is no such thing as riskless statistical arbitrage
#always check the cointegration status before trading execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import fix_yahoo_finance as yf
from sklearn.model_selection import train_test_split


# In[1]:


#check cointegration status
def cointegration(data1,data2):
    
    #train test split 
    df1,test1,df2,test2=train_test_split(data1,data2,test_size=0.7
                                         ,shuffle=False)
    
    train=pd.DataFrame()
    train['asset1']=df1['Close']
    train['asset2']=df2['Close']
    
    #this is the part where we test the cointegration
    #in this case, i use Engle-Granger two-step method
    #which is invented by the mentor of my mentor!!!
    #generally people use Johanssen test to check the cointegration status
    #the first step for EG is to run a linear regression on both variables
    #next, we do OLS and obtain the residual
    #after that we run unit root test to check the existence of cointegration
    #if it is stationary, we can determine its a drunk man with a dog
    #the first step would be adding a constant vector to asset1
    
    x=sm.add_constant(train['asset1'])
    y=train['asset2']
    model=sm.OLS(y,x).fit()
    resid=model.resid
    
    print(model.summary())
    print('\n',sm.tsa.stattools.adfuller(resid))

    #this phrase is how we set the trigger conditions
    #first we normalize the residual
    #we would get a vector that follows standard normal distribution
    #generally speaking, most tests use one sigma level as the threshold
    #two sigma level reaches 95% which is relatively difficult to trigger
    #after normalization, we should obtain a white noise follows N(0,1)
    #we set +-1 as the threshold
    #eventually we visualize the result
    
    signals=pd.DataFrame()
    signals['asset1']=test1['Close']
    signals['asset2']=test2['Close']
    
    signals['fitted']=np.mat(sm.add_constant(signals['asset2']))*np.mat(model.params).reshape(2,1)
    
    signals['residual']=signals['asset1']-signals['fitted']
    
    signals['z']=(signals['residual']-np.mean(signals['residual']))/np.std(signals['residual'])
    
    #use z*0 to get panda series instead of an integer result
    signals['z upper limit']=signals['z']*0+np.mean(signals['z'])+np.std(signals['z'])
    signals['z lower limit']=signals['z']*0+np.mean(signals['z'])-np.std(signals['z'])

    
    return signals


# In[2]:


#the signal generation process is very straight forward
#if the normalized residual gets above or below threshold
#we long the bearish one and short the bullish one, vice versa
#i only need to generate trading signal of one asset
#the other one should be the opposite direction
def signal_generation(df1,df2,method):
    
    
    signals=method(df1,df2)

    signals['signals1']=0
    
    #as z statistics cannot exceed both upper and lower bounds at the same time
    #this line holds
    signals['signals1']=np.select([signals['z']>signals['z upper limit'], \
                                   signals['z']<signals['z lower limit']], \
                                   [-1,1],default=0)
    
    #signals only imply holding
    #we take the first order difference to obtain the execution signal
    signals['positions1']=signals['signals1'].diff()
    signals['signals2']=-signals['signals1']
    signals['positions2']=signals['signals2'].diff()
    
    #fix initial positions issue
    if signals['signals1'].iloc[0]!=0:
        signals['positions1'].iloc[0]=signals['signals1'].iloc[0]
        signals['positions2'].iloc[0]=signals['signals2'].iloc[0]        
    
    return signals


# In[3]:


#position visualization
def plot(new,ticker1,ticker2):    
   
    fig=plt.figure(figsize=(10,5))
    bx=fig.add_subplot(111)   
    bx2=bx.twinx()
    
    #plot two different assets
    l1,=bx.plot(new.index,new['asset1'],
                c='#4abdac')
    l2,=bx2.plot(new.index,new['asset2'],
                 c='#907163')

    u1,=bx.plot(new.loc[new['positions1']==1].index, \
                new['asset1'][new['positions1']==1], \
                lw=0,marker='^',markersize=8, \
                c='g',alpha=0.7)
    d1,=bx.plot(new.loc[new['positions1']==-1].index, \
                new['asset1'][new['positions1']==-1], \
                lw=0,marker='v',markersize=8, \
                c='r',alpha=0.7)
    u2,=bx2.plot(new.loc[new['positions2']==1].index, \
                 new['asset2'][new['positions2']==1], \
                 lw=0,marker=2,markersize=9, \
                 c='g',alpha=0.9,markeredgewidth=3)
    d2,=bx2.plot(new.loc[new['positions2']==-1].index, \
                 new['asset2'][new['positions2']==-1], \
                 lw=0,marker=3,markersize=9, \
                 c='r',alpha=0.9,markeredgewidth=3)

    bx.set_ylabel(ticker1,)
    bx2.set_ylabel(ticker2,rotation=270)
    bx.yaxis.labelpad=15
    bx2.yaxis.labelpad=15
    bx.set_xlabel('Date')
    bx.xaxis.labelpad=15

    plt.legend([l1,l2,u1,d1,u2,d2],
               [ticker1,ticker2,
               'LONG {}'.format(ticker1),
               'SHORT {}'.format(ticker1),
               'LONG {}'.format(ticker2),
               'SHORT {}'.format(ticker2)],
               loc=8)

    plt.title('Pair Trading')
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()
  

#visualize overall portfolio performance
def portfolio(df1):

    #initial capital to calculate the actual pnl
    capital0=20000

    #shares to buy of each position
    positions1=capital0//max(df1['asset1'])
    positions2=capital0//max(df1['asset2'])

    #cumsum1 column is created to check the holding of the position
    df1['cumsum1']=df1['positions1'].cumsum()

    #since there are two assets, we calculate each asset separately
    #in the end we aggregate them into one portfolio
    portfolio=pd.DataFrame()
    portfolio['asset1']=df1['asset1']
    portfolio['holdings1']=df1['cumsum1']*df1['asset1']*positions1
    portfolio['cash1']=capital0-(df1['positions1']*df1['asset1']*positions1).cumsum()
    portfolio['total asset1']=portfolio['holdings1']+portfolio['cash1']
    portfolio['return1']=portfolio['total asset1'].pct_change()
    portfolio['positions1']=df1['positions1']
    
    df1['cumsum2']=df1['positions2'].cumsum()
    portfolio['asset2']=df1['asset2']
    portfolio['holdings2']=df1['cumsum2']*df1['asset2']*positions2
    portfolio['cash2']=capital0-(df1['positions2']*df1['asset2']*positions2).cumsum()
    portfolio['total asset2']=portfolio['holdings2']+portfolio['cash2']
    portfolio['return2']=portfolio['total asset2'].pct_change()
    portfolio['positions2']=df1['positions2']
 
    portfolio['z']=df1['z']
    portfolio['total asset']=portfolio['total asset1']+portfolio['total asset2']
    portfolio['z upper limit']=df1['z upper limit']
    portfolio['z lower limit']=df1['z lower limit']
    
    #plotting the asset value change of the portfolio
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax2=ax.twinx()
 
    l1,=ax.plot(portfolio['total asset'],c='#46344e')
    l2,=ax2.plot(portfolio['z'],c='#4f4a41',alpha=0.2)
 
    b=ax2.fill_between(portfolio.index,portfolio['z upper limit'],\
                    portfolio['z lower limit'], \
                    alpha=0.2,color='#ffb48f')
     
    #due to the opposite direction of trade for 2 assets
    #we will not plot positions on asset performance
    
    ax.set_ylabel('Asset Value')
    ax2.set_ylabel('Z Statistics',rotation=270)
    ax.yaxis.labelpad=15
    ax2.yaxis.labelpad=15
    ax.set_xlabel('Date')
    ax.xaxis.labelpad=15
    
    plt.legend([l2,b,l1],['Z Statistics',
                          'Z Statistics +-1 Sigma',
                          'Total Asset Performance'],loc='best')

    plt.grid(True)   
    plt.title('Total Asset')
    plt.show()

    return portfolio


# In[4]:


def main():
    
    #the sample i am using are NVDA and AMD from 2012 to 2015
    stdate='2013-01-01'
    eddate='2014-12-31'
    ticker1='NVDA'
    ticker2='AMD'

    df1=yf.download(ticker1,start=stdate,end=eddate)
    df2=yf.download(ticker2,start=stdate,end=eddate)
    
    signals=signal_generation(df1,df2,cointegration)
    
    plot(signals,ticker1,ticker2)
    
    portfolio(signals)

#how to calculate stats could be found from my other code called Heikin-Ashi
# https://github.com/je-suis-tm/quant-trading/blob/master/heikin%20ashi%20backtest.py
    

# In[5]:
    
if __name__ == '__main__':
    main()
