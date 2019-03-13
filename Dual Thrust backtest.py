# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 15:22:38 2018
@author: Administrator

"""
# In[1]:

#dual thrust is an opening range breakout strategy
#it is very similar to London Breakout
#please check London Breakout if u have any questions
# https://github.com/je-suis-tm/quant-trading/blob/master/London%20Breakout%20backtest.py
#Initially we set up upper and lower thresholds based on previous days open, close, high and low 
#When the market opens and the price exceeds thresholds, we would take long/short positions prior to upper/lower thresholds 
#However, there is no stop long/short position in this strategy
#We clear all positions at the end of the day
#rules of dual thrust can be found in the following link
# https://www.quantconnect.com/tutorials/dual-thrust-trading-algorithm/

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# In[2]:

os.chdir('D:/')


# In[3]:


#data frequency convertion from minute to intra daily
#as we are doing backtesting, we have already got all the datasets we need
#we can create a table to store all open, close, high and low prices
#and calculate the range before we get to signal generation
#otherwise, we would have to put this part inside the loop
#it would greatly increase the time complexity
#however, in real time trading, we do not have futures price
#we have to store all past information in sql db
#we have to calculate the range from db before the market opens

def min2day(df,column,year,month,rg):
    
    #lets create a dictionary 
    #we use keys to classify different info we need
    memo={'date':[],'open':[],'close':[],'high':[],'low':[]}
    
    #no matter which month
    #the maximum we can get is 31 days
    #thus, we only need to run a traversal on 31 days
    #nevertheless, not everyday is a workday
    #assuming our raw data doesnt contain weekend prices
    #we use try function to make sure we get the info of workdays without errors
    #note that i put date at the end of the loop
    #the date appendix doesnt depend on our raw data
    #it only relies on the range function above
    #we could accidentally append weekend date if we put it at the beginning of try function
    #not until the program cant find price in raw data will the program stop
    #by that time, we have already appended weekend date
    #we wanna make sure the length of all lists in dictionary are the same
    #so that we can construct a structured table in the next step
    for i in range(1,32):
    
        try:
            temp=df['%s-%s-%s 3:00:00'%(year,month,i):'%s-%s-%s 12:00:00'%(year,month,i)][column]

            memo['open'].append(temp[0])
            memo['close'].append(temp[-1])
            memo['high'].append(max(temp))
            memo['low'].append(min(temp))
            memo['date'].append('%s-%s-%s'%(year,month,i))
       

        except Exception:
            pass
        
    intraday=pd.DataFrame(memo)
    intraday.set_index(pd.to_datetime(intraday['date']),inplace=True)
    
    
    #preparation
    intraday['range1']=intraday['high'].rolling(rg).max()-intraday['close'].rolling(rg).min()
    intraday['range2']=intraday['close'].rolling(rg).max()-intraday['low'].rolling(rg).min()
    intraday['range']=np.where(intraday['range1']>intraday['range2'],intraday['range1'],intraday['range2'])
    
    return intraday


#signal generation
#even replace assignment with pandas.at
#it still takes a while for us to get the result
#any optimization suggestion besides using numpy array?
def signal_generation(df,intraday,param,column,rg):
    
    #as the lags of days have been set to 5  
    #we should start our backtesting after 4 workdays of current month
    #cumsum is to control the holding of underlying asset
    #sigup and siglo are the variables to store the upper/lower threshold  
    #upper and lower are for the purpose of tracking sigup and siglo
    signals=df[df.index>=intraday['date'].iloc[rg-1]]
    signals['signals']=0
    signals['cumsum']=0
    signals['upper']=0.0
    signals['lower']=0.0
    sigup=float(0)
    siglo=float(0)
    
    #for traversal on time series
    #the tricky part is the slicing
    #we have to either use [i:i] or pd.Series
    #first we set up thresholds at the beginning of london market
    #which is est 3am
    #if the price exceeds either threshold
    #we will take long/short positions  
    
    for i in signals.index:
        
        #note that intraday and dataframe have different frequencies
        #obviously different metrics for indexes
        #we use variable date for index convertion
        date='%s-%s-%s'%(i.year,i.month,i.day)
        
        
        #market opening
        #set up thresholds
        if (i.hour==3 and i.minute==0):
            sigup=float(param*intraday['range'][date]+pd.Series(signals[column])[i])
            siglo=float(-(1-param)*intraday['range'][date]+pd.Series(signals[column])[i])

        #thresholds got breached
        #signals generating
        if (sigup!=0 and pd.Series(signals[column])[i]>sigup):
            signals.at[i,'signals']=1
        if (siglo!=0 and pd.Series(signals[column])[i]<siglo):
            signals.at[i,'signals']=-1


        #check if signal has been generated
        #if so, use cumsum to verify that we only generate one signal for each situation
        if pd.Series(signals['signals'])[i]!=0:
            signals['cumsum']=signals['signals'].cumsum()        
            if (pd.Series(signals['cumsum'])[i]>1 or pd.Series(signals['cumsum'])[i]<-1):
                signals.at[i,'signals']=0
               
            #if the price goes from below the lower threshold to above the upper threshold during the day
            #we reverse our positions from short to long
            if (pd.Series(signals['cumsum'])[i]==0):
                if (pd.Series(signals[column])[i]>sigup):
                    signals.at[i,'signals']=2
                if (pd.Series(signals[column])[i]<siglo):
                    signals.at[i,'signals']=-2
                    
        #by the end of london market, which is est 12pm
        #we clear all opening positions
        #the whole part is very similar to London Breakout strategy
        if i.hour==12 and i.minute==0:
            sigup,siglo=float(0),float(0)
            signals['cumsum']=signals['signals'].cumsum()
            signals.at[i,'signals']=-signals['cumsum'][i:i]
            
        #keep track of trigger levels
        signals.at[i,'upper']=sigup
        signals.at[i,'lower']=siglo

    return signals

#plotting the positions
def plot(signals,intraday,column):
        
    #we have to do a lil bit slicing to make sure we can see the plot clearly
    #the only reason i go to -3 is that day we execute a trade    
    #give one hour before and after market trading hour for as x axis  
    date=pd.to_datetime(intraday['date']).iloc[-3]      
    signew=signals['%s-%s-%s 02:00:00'%(date.year,date.month,date.day):'%s-%s-%s 13:00:00'%(date.year,date.month,date.day)]
    
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)    
    
    #mostly the same as other py files
    #the only difference is to create an interval for signal generation
    ax.plot(signew.index,signew[column],label=column)
    ax.fill_between(signew.loc[signew['upper']!=0].index,signew['upper'][signew['upper']!=0],signew['lower'][signew['upper']!=0],alpha=0.2,color='#355c7d')
    ax.plot(signew.loc[signew['signals']==1].index,signew[column][signew['signals']==1],lw=0,marker='^',markersize=10,c='g',label='LONG')
    ax.plot(signew.loc[signew['signals']==-1].index,signew[column][signew['signals']==-1],lw=0,marker='v',markersize=10,c='r',label='SHORT')

    #change legend text color
    lgd=plt.legend(loc='best').get_texts()
    for text in lgd:
        text.set_color('#6C5B7B')

    #add some captions
    plt.text('%s-%s-%s 03:00:00'%(date.year,date.month,date.day),signew['upper']['%s-%s-%s 03:00:00'%(date.year,date.month,date.day)],'Upper Bound',color='#C06C84')
    plt.text('%s-%s-%s 03:00:00'%(date.year,date.month,date.day),signew['lower']['%s-%s-%s 03:00:00'%(date.year,date.month,date.day)],'Lower Bound',color='#C06C84')
    
    plt.ylabel(column)
    plt.xlabel('Date')
    plt.title('Dual Thrust')
    plt.grid(True)
    plt.show()



# In[4]:
def main():
    
    #similar to London Breakout
    #my raw data comes from the same website
    # http://www.histdata.com/download-free-forex-data/?/excel/1-minute-bar-quotes
    #just take the mid price of whatever currency pair you want

    df=pd.read_csv('gbpusd.csv')
    df.set_index(pd.to_datetime(df['date']),inplace=True)

    #rg is the lags of days
    #param is the parameter of trigger range, it should be smaller than one
    #normally ppl use 0.5 to give long and short 50/50 chance to trigger
    rg=5
    param=0.5

    #these three variables are for the frequency convertion from minute to intra daily
    year=df.index[0].year
    month=df.index[0].month
    column='price'
    
    intraday=min2day(df,column,year,month,rg)
    signals=signal_generation(df,intraday,param,column,rg)
    plot(signals,intraday,column)

#how to calculate stats could be found from my other code called Heikin-Ashi
# https://github.com/je-suis-tm/quant-trading/blob/master/heikin%20ashi%20backtest.py

if __name__ == '__main__':
    main()
