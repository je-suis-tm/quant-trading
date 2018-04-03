# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 20:48:35 2018

@author: Administrator
"""

#need to get fix yahoo finance package first
import pandas as pd
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import matplotlib.finance as mpf
import numpy as np
from scipy import integrate
from scipy.stats import t


#first part is about downloading data and transforming it to dataframe


stls=3
#stop loss positions, the maximum long positions we can get
ticker='NVDA'
stdate='2015-04-01'
eddate='2018-02-15'
c0=10000
#initial capital
shares=100
#shares of every position
df=yf.download(ticker,start=stdate,end=eddate)
df1=pd.DataFrame(df)
df=len(df1.index)


#details of Heikin Ashi parameters:https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx

df1['HA close']=(df1['Open']+df1['Close']+df1['High']+df1['Low'])/4
df1['HA open']=float(0)
df1['HA open'][0]=df1['Open'][0]

for n in range(1,df):
    df1['HA open'][n]=(df1['HA open'][n-1]+df1['HA close'][n-1])/2

m=pd.concat([df1['HA open'],df1['HA close'],df1['Low'],df1['High']],axis=1)
df1['HA high']=m.apply(max,axis=1)
df1['HA low']=m.apply(min,axis=1)

del df1['Adj Close']
del df1['Volume']

#setting up signal generations, details can be found from the website mentioned above, just some simple if structures

df1['signals']=0
df1['cumsum']=0

for n in range(1,df):
    if (df1['HA open'][n]>df1['HA close'][n] and df1['HA open'][n]==df1['HA high'][n] and
        np.abs(df1['HA open'][n]-df1['HA close'][n])>np.abs(df1['HA open'][n-1]-df1['HA close'][n-1]) and
        df1['HA open'][n-1]>df1['HA close'][n-1]):
        df1['signals'][n]=1
        df1['cumsum']=df1['signals'].cumsum()
        
        if df1['cumsum'][n]>stls:
            df1['signals'][n]=0
        

    elif (df1['HA open'][n]<df1['HA close'][n] and df1['HA open'][n]==df1['HA low'][n] and 
    df1['HA open'][n-1]<df1['HA close'][n-1]):
        df1['signals'][n]=-1
        df1['cumsum']=df1['signals'].cumsum()
        
        if df1['cumsum'][n]>0:
            df1['signals'][n]=-1*(df1['cumsum'][n-1])
        elif df1['cumsum'][n]<0:
            df1['signals'][n]=0
            

#plotting the backtesting result, first plot is Heikin-Ashi candlestick, the second plot is the actual price with long/short positions


ax1=plt.subplot2grid((200,1), (0,0), rowspan=120,ylabel='HA price')
mpf.candlestick2_ochl(ax1, df1['HA open'], df1['HA close'], df1['HA high'], df1['HA low'], width=1, colorup='g', colordown='r')
plt.grid(True)
plt.xticks([])
plt.title('Heikin-Ashi')

ax2=plt.subplot2grid((200,1), (120,0), rowspan=80,ylabel='price',xlabel='')
df1['Close'].plot(ax=ax2,label=ticker,c='k')
#long/short positions are attached to the real close price of the stock
ax2.plot(df1.loc[df1['signals']==1].index,df1['Close'][df1['signals']==1],marker='^',lw=0,c='g',label='long')
ax2.plot(df1.loc[df1['signals']<0].index,df1['Close'][df1['signals']<0],marker='v',lw=0,c='r',label='short')
plt.grid(True)
plt.legend(loc=0)
plt.show()

#backtesting
#cumsum column is created to check the holding of the position
df1['cumsum']=df1['signals'].cumsum()
pos=shares*df1['signals']
portfolio=pd.DataFrame(index=df1.index)
portfolio['holdings']=df1['cumsum']*df1['Close']*shares
portfolio['cash']=c0-(pos.multiply(df1['Close'],axis=0)).cumsum()
portfolio['total asset']=portfolio['holdings']+portfolio['cash']
portfolio['return']=portfolio['total asset'].pct_change()
portfolio['close']=df1['Close']
portfolio['signals']=df1['signals']

#plotting the change of total asset value
fig=plt.figure()
bx=fig.add_subplot(111)
portfolio['total asset'].plot()
#long/short positions related to the portfolio
bx.plot(portfolio['signals'].loc[portfolio['signals']==1].index,portfolio['total asset'][portfolio['signals']==1],lw=0,marker='^',c='g',label='long')
bx.plot(portfolio['signals'].loc[portfolio['signals']<0].index,portfolio['total asset'][portfolio['signals']<0],lw=0,marker='v',c='r',label='short')
plt.legend(loc='best')
plt.grid(True)
plt.xlabel('date')
plt.ylabel('asset value')

plt.show()

#ratio calculation begins
a=np.arange(1).reshape(1,1)
stats=pd.DataFrame(a)
#get the min and max of return
sigu=np.max(portfolio['return'])
sigl=np.min(portfolio['return'])
#m is the average growth rate of portfolio return
m=(float(portfolio['total asset'][-1:]/c0))**(1/df)-1
#calculating the standard deviation
std=float(np.sqrt((((portfolio['return']-m)**2).sum())/df))


#use S&P500 as benchmark
benchmark=yf.download('^GSPC',start=stdate,end=eddate)
#rb is the return of benchmark
rb=float(benchmark['Close'][-1:]/benchmark['Open'][0]-1)
#rf is the average growth rate of benchmark return
rf=(rb+1)**(1/df)-1
del benchmark


#omega ratio is a variation of sharpe ratio, the risk free return is replaced by a given threshhold, in this case, the return of benchmark, integration is needed to calculate the return above and below the threshold


def omega(rf,df,sigu,sigl):
    y=integrate.quad(lambda g:1-t.cdf(g,df),rf,sigu)
    x=integrate.quad(lambda g:t.cdf(g,df),sigl,rf)
    z=(y[0])/(x[0])
    return z

#sortino ratio is another variation of sharpe ratio, the standard deviation of all returns is substituted with standard deviation of negative returns which calculated by integration


def sortino(rf,df,m,sigl):
    v=np.sqrt(np.abs(integrate.quad(lambda r:((rf-r)**2)*t.pdf(r,df),rf,sigl)))
    s=(m-rf)/v[0]
    return s


#backtesting stats
stats['CAGR']=stats['portfolio return']=float(0)
stats['CAGR'][0]=m
stats['portfolio return'][0]=portfolio['total asset'][-1:]/c0-1
stats['benchmark return']=rb
stats['sharpe ratio']=(m-rf)/std
stats['maximum drawdown']=np.min(portfolio['total asset'])/np.max(portfolio['total asset'])-1
stats['calmar ratio']=m/stats['maximum drawdown']
stats['omega ratio']=omega(rf,df,sigu,sigl)
stats['sortino ratio']=sortino(rf,df,m,sigl)
stats['numbers of longs']=df1['signals'].loc[df1['signals']==1].count()
stats['numbers of shorts']=df1['signals'].loc[df1['signals']<0].count()
stats['numbers of trades']=stats['numbers of shorts']+stats['numbers of longs']  
stats['total length of trades']=df1['signals'].loc[df1['cumsum']!=0].count()
stats['average length of trades']=stats['total length of trades']/stats['numbers of trades']
stats['profit per trade']=float(0)
stats['profit per trade'][0]=(portfolio['total asset'][-1:]-c0)/stats['numbers of trades'][0]

#
print(stats)