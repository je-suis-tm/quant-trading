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



#stop loss positions, the maximum long positions we can get
#without certain constraints, you will long indefinites times as long as the market condition triggers the signal
#in a bear market, it is suicidal
stls=3
ticker='NVDA'
stdate='2015-04-01'
eddate='2018-02-15'
#initial capital to calculate the actual pnl
c0=10000
#shares of every position
shares=100

df=yf.download(ticker,start=stdate,end=eddate)
df1=pd.DataFrame(df)
df=len(df1.index)


#details of Heikin Ashi parameters:https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx
#Heikin Ashi has a unique method to filter out the noise
#its open, close, high, low require a different calculation approach
#please refer to the website mentioned above

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

#setting up signal generations
#trigger conditions can be found from the website mentioned above
#there should also be a short strategy
#as i am an individual investor, i only use long and clear strategies
#the trigger condition of short strategy is the reverse of long strategy
#you have to satisfy all four conditions to long/short
#nevertheless, the clear signal only has three conditions

df1['signals']=0
#i use cumulated sum to check how many positions i have longed
#i would ignore the clear signal prior to no long positions in the portfolio
#i also keep tracking how many long positions i have got
#long signals cannot exceed the stop loss limit
df1['cumsum']=0

#bear in mind that df was a dataframe
#i reassign it to represent the length of the dataframe
for n in range(1,df):
    if (df1['HA open'][n]>df1['HA close'][n] and df1['HA open'][n]==df1['HA high'][n] and
        np.abs(df1['HA open'][n]-df1['HA close'][n])>np.abs(df1['HA open'][n-1]-df1['HA close'][n-1]) and
        df1['HA open'][n-1]>df1['HA close'][n-1]):
        df1['signals'][n]=1
        df1['cumsum']=df1['signals'].cumsum()
        
        #stop longing positions
        if df1['cumsum'][n]>stls:
            df1['signals'][n]=0
        

    elif (df1['HA open'][n]<df1['HA close'][n] and df1['HA open'][n]==df1['HA low'][n] and 
    df1['HA open'][n-1]<df1['HA close'][n-1]):
        df1['signals'][n]=-1
        df1['cumsum']=df1['signals'].cumsum()
        
        #if long positions i hold are more than one
        #its time to clear all my positions
        #if there are no long positions in my portfolio
        #ignore the clear signal
        if df1['cumsum'][n]>0:
            df1['signals'][n]=-1*(df1['cumsum'][n-1])
        elif df1['cumsum'][n]<0:
            df1['signals'][n]=0
            

#plotting the backtesting result
#first plot is Heikin-Ashi candlestick
#use candlestick function and set Heikin-Ashi O,C,H,L
#the second plot is the actual price with long/short positions as up/down arrows


ax1=plt.subplot2grid((200,1), (0,0), rowspan=120,ylabel='HA price')
mpf.candlestick2_ochl(ax1, df1['HA open'], df1['HA close'], df1['HA high'], df1['HA low'], width=1, colorup='g', colordown='r')
plt.grid(True)
plt.xticks([])
plt.title('Heikin-Ashi')

ax2=plt.subplot2grid((200,1), (120,0), rowspan=80,ylabel='price',xlabel='')
df1['Close'].plot(ax=ax2,label=ticker,c='k')
#long/short positions are attached to the real close price of the stock
#set the line width to zero
#thats why we only observe markers
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

#plotting the asset value change of the portfolio
fig=plt.figure()
bx=fig.add_subplot(111)
portfolio['total asset'].plot()
#long/short position markers related to the portfolio
#the same mechanism as the previous one
#replace close price with total asset value
bx.plot(portfolio['signals'].loc[portfolio['signals']==1].index,portfolio['total asset'][portfolio['signals']==1],lw=0,marker='^',c='g',label='long')
bx.plot(portfolio['signals'].loc[portfolio['signals']<0].index,portfolio['total asset'][portfolio['signals']<0],lw=0,marker='v',c='r',label='short')
plt.legend(loc='best')
plt.grid(True)
plt.xlabel('date')
plt.ylabel('asset value')

plt.show()

#ratio calculation begins

stats=pd.DataFrame([0])

#get the min and max of return
sigu=np.max(portfolio['return'])
sigl=np.min(portfolio['return'])
#m is the average growth rate of portfolio 
#i use geometric average instead of arithmetic average for percentage growth
m=(float(portfolio['total asset'][-1:]/c0))**(1/df)-1
#calculating the standard deviation
std=float(np.sqrt((((portfolio['return']-m)**2).sum())/df))


#use S&P500 as benchmark
benchmark=yf.download('^GSPC',start=stdate,end=eddate)
#rb is the return of benchmark
rb=float(benchmark['Close'][-1:]/benchmark['Open'][0]-1)
#rf is the average growth rate of benchmark 
#i use geometric average instead of arithmetic average for percentage growth
rf=(rb+1)**(1/df)-1
del benchmark


#omega ratio is a variation of sharpe ratio
#the risk free return is replaced by a given threshhold
#in this case, the return of benchmark
#integration is needed to calculate the return above and below the threshold
#it is a more reasonable ratio to measure the risk adjusted return
#normal distribution doesnt explain the fat tail of returns
#so i use student T cumulated distribution function instead 
#for reason of simplicity, i do not use empirical distribution
#the cdf of empirical distribution is much more complex
def omega(rf,df,sigu,sigl):
    y=integrate.quad(lambda g:1-t.cdf(g,df),rf,sigu)
    x=integrate.quad(lambda g:t.cdf(g,df),sigl,rf)
    z=(y[0])/(x[0])
    return z

#sortino ratio is another variation of sharpe ratio
#the standard deviation of all returns is substituted with standard deviation of negative returns
#sortino ratio measures the impact of negative return on return
#i am also using student T probability distribution function instead of normal distribution

def sortino(rf,df,m,sigl):
    v=np.sqrt(np.abs(integrate.quad(lambda r:((rf-r)**2)*t.pdf(r,df),rf,sigl)))
    s=(m-rf)/v[0]
    return s

#this is how to calculate the maximum drawdown
#basically we take return of every period
#we check the difference between return and previous maximum return
#we get the drawdown
#we set a variable to store every day drawdown
#when the new drawdown is smaller than the variable
#we update the variable with the smaller one
#in the end we output the mininum value which is the maximum drawdown
#cuz drawdown is negative so this is called maximum drawdown
def mdd(list):
    temp=0
    for i in range(1,len(list)):
        if temp>(list[i]/max(list[:i])-1):
            temp=(list[i]/max(list[:i])-1)

    return temp

#backtesting stats
#CAGR stands for cumulated average growth rate
stats['CAGR']=stats['portfolio return']=float(0)
stats['CAGR'][0]=m
stats['portfolio return'][0]=portfolio['total asset'][-1:]/c0-1
stats['benchmark return']=rb
stats['sharpe ratio']=(m-rf)/std
stats['maximum drawdown']=mdd(portfolio['total asset'])
#calmar ratio is sorta like sharpe ratio
#the standard deviation is replaced by maximum drawdown
#it is the measurement of return after worse scenario adjustment
stats['calmar ratio']=m/stats['maximum drawdown']
stats['omega ratio']=omega(rf,df,sigu,sigl)
stats['sortino ratio']=sortino(rf,df,m,sigl)
#note that i use stop loss limit to limit the numbers of longs
#and when clearing positions, we clear all the positions at once
#so every long is always one, and short could be no larger than the stop loss limit
stats['numbers of longs']=df1['signals'].loc[df1['signals']==1].count()
stats['numbers of shorts']=df1['signals'].loc[df1['signals']<0].count()
stats['numbers of trades']=stats['numbers of shorts']+stats['numbers of longs']  
#to get the total length of trades
#given that cumsum indicates the holding of positions
#we can get all the possible outcomes when cumsum doesnt equal zero
#then we count how many non-zero positions there are
#we get the estimation of total length of trades
stats['total length of trades']=df1['signals'].loc[df1['cumsum']!=0].count()
stats['average length of trades']=stats['total length of trades']/stats['numbers of trades']
stats['profit per trade']=float(0)
stats['profit per trade'][0]=(portfolio['total asset'][-1:]-c0)/stats['numbers of trades'][0]

#
print(stats)
