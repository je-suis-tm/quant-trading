# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 15:22:38 2018

@author: Administrator
"""

import os
os.chdir('D:/')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#
df=pd.read_csv('eurusd.csv')
df.set_index(pd.to_datetime(df['date']),inplace=True)

rg=5
param=0.5



#as we are doing backtesting, we have already got all the datasets we need
#we can create a table to store all open, close, high and low prices
#and calculate the range before we get to signal generation
#otherwise, we would have to put this part inside the loop
#it would greatly increase the time complexity
#however, in real time trading, we do not have futures price
#we have to store all past information in sql
#we have to calculate the range from sql before the market opens

#lets create a dictionary 
#we use keys to classify different info we need
memo={'date':[],'open':[],'close':[],'high':[],'low':[]}
for i in range(1,32):
    #as we already know we use january price to do backtesting
    #we only need to run a traversal on 31 days
    #nevertheless, not everyday is a workday
    #assuming our raw data doesnt contain weekend prices
    #we use try function to make sure we get the info of workdays without errors
    #note that i put date at the end of the loop
    #the date appendix doesnt depend on our raw data
    #it only relies on the range function above
    #we could accidentally append weekend date if we put it at the beginning
    #not until the program cant find price in raw data will the program stop
    #by that time, we have already appended weekend date
    #we wanna make sure the length of all lists in dictionary are the same
    #so that we can construct a structured table in the next step
    try:
        temp=df['2018-01-%d 3:00:00'%(i):'2018-01-%d 12:00:00'%(i)]['eurusd']
        
        memo['open'].append(temp[0])
        memo['close'].append(temp[-1])
        memo['high'].append(max(temp))
        memo['low'].append(min(temp))
        memo['date'].append('2018-01-%d'%(i))
        
    except Exception:
        continue

intraday=pd.DataFrame()
for key in memo:
    intraday[key]=memo[key]

intraday.set_index(pd.to_datetime(intraday['date']),inplace=True)
intraday['range1']=intraday['high'].rolling(rg).max()-intraday['close'].rolling(rg).min()
intraday['range2']=intraday['close'].rolling(rg).max()-intraday['low'].rolling(rg).min()
intraday['range']=np.where(intraday['range1']>intraday['range2'],intraday['range1'],intraday['range2'])
    

    
#as the lags of days have been set to 5
#we should start our backtesting after 4 workdays of january
#which is jan 8
#cumsum is to control the holding of underlying asset
#sigup and siglo are the variables to store the upper/lower threshold
signals=pd.DataFrame(df[df.index>='2018-01-08'])
signals['signals']=0
signals['cumsum']=0
sigup=float(0)
siglo=float(0)


#for traversal on time series
#the tricky part is the slicing
#we have to either use [i:i] or pd.Series
#first we set up thresholds at the beginning of london market
#which is est 3am
#if the price exceeds either threshold
#we will take long/short positions
#cumsum is used to make sure that we only generate one signal for each situation
#if the price goes from below the lower threshold to above the upper threshold during the day
#we reverse our positions from short to long
#by the end of london market, which is est 12pm
#we clear all opening positions
#the whole part is very similar to London Breakout strategy
for i in signals.index:
    if (i.hour==3 and i.minute==0):
        sigup=float(param*intraday['range']['2018-01-%d'%(i.day):'2018-01-%d'%(i.day)]+pd.Series(signals['eurusd'])[i])
        siglo=float(-(1-param)*intraday['range']['2018-01-%d'%(i.day):'2018-01-%d'%(i.day)]+pd.Series(signals['eurusd'])[i])

    if (sigup!=0 and pd.Series(signals['eurusd'])[i]>sigup):
        signals['signals'][i:i]=1
    if (siglo!=0 and pd.Series(signals['eurusd'])[i]<siglo):
        signals['signals'][i:i]=-1

    if pd.Series(signals['signals'])[i]!=0:
        signals['cumsum']=signals['signals'].cumsum()
        
        if (pd.Series(signals['cumsum'])[i]>1 or pd.Series(signals['cumsum'])[i]<-1):
            signals['signals'][i:i]=0
               
        if (pd.Series(signals['cumsum'])[i]==0):
            if (pd.Series(signals['eurusd'])[i]>sigup):
                signals['signals'][i:i]=2
            if (pd.Series(signals['eurusd'])[i]<siglo):
                signals['signals'][i:i]=-2
  
    if i.hour==12 and i.minute==0:
        sigup,siglo=float(0),float(0)
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][i:i]=-signals['cumsum'][i:i]
        

#in the end, we plot our positions throughout january
#this time, lets use ggplot for a different experience
#we always need to set up the style before we begin to plot
plt.style.use('ggplot')
plt.show()
#we have to do a lil bit slicing to make sure we can see the plot clearly
signew=signals[signals.index>'2018-01-20']
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(signew['eurusd'],label='EURUSD')
ax.plot(signew.loc[signew['signals']==1].index,signew['eurusd'][signew['signals']==1],lw=0,marker='^',markersize=10,c='g',label='long')
ax.plot(signew.loc[signew['signals']==-1].index,signew['eurusd'][signew['signals']==-1],lw=0,marker='v',markersize=10,c='r',label='short')
#somehow ggplot legends use white texts as default
#this is how we change that
lgd=plt.legend(loc='best').get_texts()
for text in lgd:
    text.set_color('k')
plt.ylabel('EURUSD')
plt.xlabel('date')
plt.title('positions')
plt.show()
