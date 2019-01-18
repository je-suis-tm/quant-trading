# coding: utf-8

# In[1]:

#assuming you already know how monte carlo works
#if not, plz click the link below
# https://datascienceplus.com/how-to-apply-monte-carlo-simulation-to-forecast-stock-prices-using-python/

#monte carlo simulation is a buzz word for people outside of financial industry
#in the industry, everybody jokes about it but no one actually uses it
#including my risk quant friends, they be like why the heck use that
#you may argue its application in option pricing to monitor fat tail events
#seriously, did anyone predict 2008 financial crisis?
#or did anyone foresee the vix surging in early 2018?

#the weakness of monte carlo, perhaps in every forecast methodology
#is that our pseudo random number is generated via empirical distribution
#in another word, we use the past to predict the future
#if something has never happened in the past
#how can you predict it with our limited imagination
#its like muggles trying to understand the wizard world
#laplace smoothing is actually better than monte carlo in this case

#the idea presented here is very straight forward
#we construct a model to get mean and variance of its residual (return)
#we generate the next possible price by geometric brownian motion
#we run this simulations as many times as possible
#naturally we should acquire a large amount of data in the end
#we pick the forecast that has the least std against the original data series
#we would check if the best forecast can predict the future direction (instead of actual price)
#and how well monte carlo catches black swans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import random as rd
from sklearn.model_selection import train_test_split


# In[2]:

#this list is purely designed to generate gradient color 
global colorlist
colorlist=['#fffb77',
 '#fffa77',
 '#fff977',
 '#fff876',
 '#fff776',
 '#fff676',
 '#fff576',
 '#fff475',
 '#fff375',
 '#fff275',
 '#fff175',
 '#fff075',
 '#ffef74',
 '#ffef74',
 '#ffee74',
 '#ffed74',
 '#ffec74',
 '#ffeb73',
 '#ffea73',
 '#ffe973',
 '#ffe873',
 '#ffe772',
 '#ffe672',
 '#ffe572',
 '#ffe472',
 '#ffe372',
 '#ffe271',
 '#ffe171',
 '#ffe071',
 '#ffdf71',
 '#ffde70',
 '#ffdd70',
 '#ffdc70',
 '#ffdb70',
 '#ffda70',
 '#ffd96f',
 '#ffd86f',
 '#ffd76f',
 '#ffd66f',
 '#ffd66f',
 '#ffd56e',
 '#ffd46e',
 '#ffd36e',
 '#ffd26e',
 '#ffd16d',
 '#ffd06d',
 '#ffcf6d',
 '#ffce6d',
 '#ffcd6d',
 '#ffcc6c',
 '#ffcb6c',
 '#ffca6c',
 '#ffc96c',
 '#ffc86b',
 '#ffc76b',
 '#ffc66b',
 '#ffc56b',
 '#ffc46b',
 '#ffc36a',
 '#ffc26a',
 '#ffc16a',
 '#ffc06a',
 '#ffbf69',
 '#ffbe69',
 '#ffbd69',
 '#ffbd69',
 '#ffbc69',
 '#ffbb68',
 '#ffba68',
 '#ffb968',
 '#ffb868',
 '#ffb768',
 '#ffb667',
 '#ffb567',
 '#ffb467',
 '#ffb367',
 '#ffb266',
 '#ffb166',
 '#ffb066',
 '#ffaf66',
 '#ffad65',
 '#ffac65',
 '#ffab65',
 '#ffa964',
 '#ffa864',
 '#ffa763',
 '#ffa663',
 '#ffa463',
 '#ffa362',
 '#ffa262',
 '#ffa062',
 '#ff9f61',
 '#ff9e61',
 '#ff9c61',
 '#ff9b60',
 '#ff9a60',
 '#ff9860',
 '#ff975f',
 '#ff965f',
 '#ff955e',
 '#ff935e',
 '#ff925e',
 '#ff915d',
 '#ff8f5d',
 '#ff8e5d',
 '#ff8d5c',
 '#ff8b5c',
 '#ff8a5c',
 '#ff895b',
 '#ff875b',
 '#ff865b',
 '#ff855a',
 '#ff845a',
 '#ff8259',
 '#ff8159',
 '#ff8059',
 '#ff7e58',
 '#ff7d58',
 '#ff7c58',
 '#ff7a57',
 '#ff7957',
 '#ff7857',
 '#ff7656',
 '#ff7556',
 '#ff7455',
 '#ff7355',
 '#ff7155',
 '#ff7054',
 '#ff6f54',
 '#ff6d54',
 '#ff6c53',
 '#ff6b53',
 '#ff6953',
 '#ff6852',
 '#ff6752',
 '#ff6552',
 '#ff6451',
 '#ff6351',
 '#ff6250',
 '#ff6050',
 '#ff5f50',
 '#ff5e4f',
 '#ff5c4f',
 '#ff5b4f',
 '#ff5a4e',
 '#ff584e',
 '#ff574e',
 '#ff564d',
 '#ff544d',
 '#ff534d',
 '#ff524c',
 '#ff514c',
 '#ff4f4b',
 '#ff4e4b',
 '#ff4d4b',
 '#ff4b4a',
 '#ff4a4a']


# In[3]:


#this is where the actual simulation happens
#testsize denotes how much percentage of dataset would be used for testing
#simulation denotes the number of simulations
#theoretically speaking, the larger the better
#given the constrained computing power
#we have to take a balance point between efficiency and effectiveness
def monte_carlo(data,testsize=0.5,simulation=100,**kwargs):    
    
    #train test split as usual
    df,test=train_test_split(data,test_size=testsize,shuffle=False,**kwargs)
    forecast_horizon=len(test)
    
    #we only care about close price
    #if there has been dividend issued
    #we use adjusted close price instead
    df=df.loc[:,['Close']]
        
    #here we use log return
    returnn=np.log(df['Close'].iloc[1:]/df['Close'].shift(1).iloc[1:])
    drift=returnn.mean()-returnn.var()/2
    
    #we use dictionary to store predicted time series
    d={}
    
    #we use geometric brownian motion to compute the next price
    # https://en.wikipedia.org/wiki/Geometric_Brownian_motion
    for counter in range(simulation):
        d[counter]=[df['Close'].iloc[0]]
      
        #we dont just forecast the future
        #we need to compare the forecast with the historical data as well
        #thats why the data range is training horizon plus testing horizon
        for i in range(len(df)+forecast_horizon-1):
         
            #we use standard normal distribution to generate pseudo random number
            #which is sufficient for our monte carlo simulation
            sde=drift+returnn.std()*rd.gauss(0,1)
            temp=d[counter][-1]*np.exp(sde)
        
            d[counter].append(temp.item())
    
    #to determine which simulation is the best fit
    #we use simple criterias, the smallest standard deviation
    #we iterate through every simulation and compare it with actual data
    #the one with the least standard deviation wins
    std=float('inf')
    pick=0
    for counter in range(simulation):
    
        temp=np.std(np.subtract(
                    d[counter][:len(df)],df['Close']))
        if temp<std:
            std=temp
            pick=counter
    
    return forecast_horizon,d,pick


# In[4]:

#result plotting
def plot(df,forecast_horizon,d,pick,ticker):
    
    #the first plot is to plot every simulation
    #and highlight the best fit with the actual dataset
    #we only look at training horizon in the first figure
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i in range(int(len(d))):
        if i!=pick:
            ax.plot(df.index[:len(df)-forecast_horizon], \
                    d[i][:len(df)-forecast_horizon], \
                    alpha=0.05)
    ax.plot(df.index[:len(df)-forecast_horizon], \
            d[pick][:len(df)-forecast_horizon], \
            c='#5398d9',linewidth=5,label='Best Fitted')
    df['Close'].iloc[:len(df)-forecast_horizon].plot(c='#d75b66',linewidth=5,label='Actual')
    plt.title(f'Monte Carlo Simulation\nTicker: {ticker}')
    plt.legend(loc=0)
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()
    
    #the second figure plots both training and testing horizons
    #we compare the best fitted plus forecast with the actual history
    #the figure reveals why monte carlo simulation in trading is house of cards
    #it is merely illusion that monte carlo simulation can forecast any asset price or direction
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.plot(d[pick],label='Best Fitted',c='#edd170')
    plt.plot(df['Close'].tolist(),label='Actual',c='#02231c')
    plt.axvline(len(df)-forecast_horizon,linestyle=':',c='k')
    plt.text(len(df)-forecast_horizon-50, \
             max(max(df['Close']),max(d[pick])),'Training', \
             horizontalalignment='center', \
             verticalalignment='center')
    plt.text(len(df)-forecast_horizon+50, \
             max(max(df['Close']),max(d[pick])),'Testing', \
             horizontalalignment='center', \
             verticalalignment='center')
    plt.title(f'Training versus Testing\nTicker: {ticker}\n')
    plt.legend(loc=0)
    plt.ylabel('Price')
    plt.xlabel('T+Days')
    plt.show()


# In[5]:

#we also gotta test if the surge in simulations increases the prediction accuracy
#simu_start denotes the minimum simulation number
#simu_end denotes the maximum simulation number
#sim_delta denotes how many steps it takes to reach the max from the min
#its kinda like range(simu_start,simu_end,simu_delta)
def test(df,ticker,simu_start=100,simu_end=1000,simu_delta=100,**kwargs):
    
    table=pd.DataFrame()
    table['Simulations']=np.arange(simu_start,simu_end+simu_delta,simu_delta)
    table.set_index('Simulations',inplace=True)
    table['Prediction']=0

    #for each simulation
    #we test if the prediction is accurate
    #for instance
    #if the end of testing horizon is larger than the end of training horizon
    #we denote the return direction as +1
    #if both actual and predicted return direction align
    #we conclude the prediction is accurate
    #vice versa
    for i in np.arange(simu_start,simu_end+1,simu_delta):
        print(i)
        
        forecast_horizon,d,pick=monte_carlo(df,simulation=i,**kwargs)
        
        actual_return=np.sign( \
                              df['Close'].iloc[len(df)-forecast_horizon]-df['Close'].iloc[-1])
        
        best_fitted_return=np.sign(d[pick][len(df)-forecast_horizon]-d[pick][-1])
        table.at[i,'Prediction']=np.where(actual_return==best_fitted_return,1,-1)
        
    #we plot the horizontal bar chart 
    #to show the accuracy does not increase over the number of simulations
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['right'].set_position('center')
    ax.spines['top'].set_visible(False)

    plt.barh(np.arange(1,len(table)*2+1,2),table['Prediction'], \
             color=colorlist[0::int(len(colorlist)/len(table))])

    plt.xticks([-1,1],['Failure','Success'])
    plt.yticks(np.arange(1,len(table)*2+1,2),table.index)
    plt.xlabel('Prediction Accuracy')
    plt.ylabel('Times of Simulation')
    plt.title(f"Prediction accuracy doesn't depend on the numbers of simulation.\nTicker: {ticker}\n")
    plt.show()


# In[6]:

#lets try something extreme, pick ge, the worst performing stock in 2018
#see how monte carlo works for both direction prediction and fat tail simulation
#why the extreme? well if we are risk quants, we care about value at risk, dont we
#if quants only look at one sigma event, the portfolio performance would be devastating
def main():
    
    stdate='2016-01-15'
    eddate='2019-01-15'
    ticker='GE'

    df=yf.download(ticker,start=stdate,end=eddate)
    df.index=pd.to_datetime(df.index)
    
    forecast_horizon,d,pick=monte_carlo(df)
    plot(df,forecast_horizon,d,pick,ticker)
    test(df,ticker)


if __name__ == '__main__':
    main()
