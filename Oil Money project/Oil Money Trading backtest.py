
# coding: utf-8

# In[1]:


#here is the official trading strategy script for this lil project
#the details could be found in the readme of the repo, section norwegian krone and brent crude
# https://github.com/je-suis-tm/quant-trading/blob/master/Oil%20Money%20project/README.md
import statsmodels.api as sm
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('d:/')


# In[2]:

#theoratically we only need two sigma to trigger the trading signals
#i only add one sigma to make it look better in visualization
def oil_money(dataset):
    
    df=copy.deepcopy(dataset)
    
    df['signals']=0
    df['pos2 sigma']=0.0
    df['neg2 sigma']=0.0
    df['pos1 sigma']=0.0
    df['neg1 sigma']=0.0
    df['forecast']=0.0
    
    return df


# In[3]:

#the trading idea is straight forward
#we run regression on nok and brent of the past 50 data points by default
#if the rsquared exceeds 0.7 by default
#the regression model is deemed valid
#we calculate the standard deviation of the residual
#and use +/- two sigma as the threshold to trigger the trading signals
#once the trade is executed
#we would start a counter to count the period of position holding
#if the holding period exceeds 10 days by default
#we clear our positions
#meanwhile, if the spread between current price and entry price exceeds stop limit
#which is 0.5 points by default in both ways
#we clear our positions to claim profit/loss
#once our positions are cleared
#we recalibrate our regression model based on the latest 50 data points
#we keep doing this on and on
def signal_generation(dataset,x,y,method, \
                      holding_threshold=10, \
                      stop=0.5,rsquared_threshold=0.7, \
                      train_len=50):
    
    df=method(dataset)
    
    #variable holding takes 3 values, -1,0,1
    #0 implies no holding positions
    #1 implies long, -1 implies short
    #when we wanna clear our positions
    #we just reverse the sign of holding
    #which is quite convenient
    holding=0
    
    #trained is a boolean value
    #it indicates whether the current model is valid
    #in another word,when trained==True, r squared is over 0.7 by default
    #and the regressand is within two sigma range from the fitted value
    trained=False
    
    #counter counts the days of position holding
    counter=0
    

    for i in range(train_len,len(df)):
        
        #when we have uncleared positions
        if holding!=0:
            
            #when counter exceeds holding threshold
            #we clear our positions and reset all the parameters
            if counter>holding_threshold:
                df.at[i,'signals']=-holding            
                holding=0
                trained=False
                counter=0
                
                #we use continue to skip this round of iteration
                #only if the clearing condition gets triggered
                continue
                
            #plz note i make stop loss and stop profit symmetric
            #thats why we use absolute value of the spread between current price and entry price
            #usually stop loss and stop profit are asymmetric 
            #as ppl cannot take as much loss as profit
            if np.abs( \
                      df[y].iloc[i]-df[y][df['signals']!=0].iloc[-1] \
                      )>=stop:
                df.at[i,'signals']=-holding        
                holding=0
                trained=False
                counter=0
            
                continue
        
            counter+=1
    
        else:
            
            #if we do not have a valid model yet
            #we would keep trying the latest 50 data points
            if not trained:
                X=sm.add_constant(df[x].iloc[i-train_len:i])
                Y=df[y].iloc[i-train_len:i]
                m=sm.OLS(Y,X).fit()
                
                #if r squared meets the statistical request
                #which is 0.7 by default
                #we can start to build up confidence intervals
                if m.rsquared>rsquared_threshold:
                    trained=True
                    sigma=np.std(Y-m.predict(X))
                    
                    #plz note that we set the forecast and confidence intervals
                    #for every data point after the current one
                    #this would fill in the blank once our model turns invalid
                    #when we have a new valid model
                    #the new forecast and confidence intervals would cover the former one
                    df.at[i:,'forecast']= \
                    m.predict(sm.add_constant(df[x].iloc[i:]))
                    
                    df.at[i:,'pos2 sigma']= \
                    df['forecast'].iloc[i:]+2*sigma
                    
                    df.at[i:,'neg2 sigma']= \
                    df['forecast'].iloc[i:]-2*sigma
                    
                    df.at[i:,'pos1 sigma']= \
                    df['forecast'].iloc[i:]+sigma
                    
                    df.at[i:,'neg1 sigma']= \
                    df['forecast'].iloc[i:]-sigma
            
            #once we have a valid model
            #we can feel free to generate trading signals
            if trained:
                if df[y].iloc[i]>df['pos2 sigma'].iloc[i]:
                    df.at[i,'signals']=1
                    holding=1
                    
                    #once the positions are entered
                    #we set confidence intervals back to the fitted value
                    #so we could avoid the confusion in our visualization
                    #for instance. if we dont do that, 
                    #there would be confidence intervals even when the model is broken
                    #we could have been asking why no trade has been executed,
                    #even when actual price falls out of the confidence intervals?
                    df.at[i:,'pos2 sigma']=df['forecast']
                    df.at[i:,'neg2 sigma']=df['forecast']
                    df.at[i:,'pos1 sigma']=df['forecast']
                    df.at[i:,'neg1 sigma']=df['forecast']
                    
                if df[y].iloc[i]<df['neg2 sigma'].iloc[i]:
                    df.at[i,'signals']=-1
                    holding=-1
                    
                    df.at[i:,'pos2 sigma']=df['forecast']
                    df.at[i:,'neg2 sigma']=df['forecast']
                    df.at[i:,'pos1 sigma']=df['forecast']
                    df.at[i:,'neg1 sigma']=df['forecast']

                    
    return df
    


# In[4]:

#this part is to monitor how our portfolio performs over time
#details can be found from heiki ashi
# https://github.com/je-suis-tm/quant-trading/blob/master/Heikin-Ashi%20backtest.py
def portfolio(signals,close_price,capital0=5000):   
    
    positions=capital0//max(signals[close_price])
    portfolio=pd.DataFrame()
    portfolio['close']=signals[close_price]
    portfolio['signals']=signals['signals']
    
    portfolio['holding']=portfolio['signals'].cumsum()* \
    portfolio['close']*positions

    portfolio['cash']=capital0-(portfolio['signals']* \
                                portfolio['close']*positions).cumsum()
   
    portfolio['asset']=portfolio['holding']+portfolio['cash']
    

    return portfolio


# In[5]:

#plotting fitted vs actual price with confidence intervals and positions
def plot(signals,close_price):
    
    data=copy.deepcopy(signals[signals['forecast']!=0])
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    data['forecast'].plot(label='Fitted',color='#f4f4f8',alpha=0.7)
    data[close_price].plot(label='Actual',color='#3c2f2f',alpha=0.7)
    
    ax.fill_between(data.index,data['pos1 sigma'], \
                    data['neg1 sigma'],alpha=0.3, \
                    color='#011f4b', label='1 Sigma')
    ax.fill_between(data.index,data['pos2 sigma'], \
                    data['neg2 sigma'],alpha=0.3, \
                    color='#ffc425', label='2 Sigma')
    
    ax.plot(data.loc[data['signals']==1].index, \
            data[close_price][data['signals']==1],marker='^', \
            c='#00b159',linewidth=0,label='LONG',markersize=11, \
            alpha=1)
    ax.plot(data.loc[data['signals']==-1].index, \
            data[close_price][data['signals']==-1],marker='v', \
            c='#ff6f69',linewidth=0,label='SHORT',markersize=11, \
            alpha=1)
    
    plt.title(f'Oil Money Project\n{close_price.upper()} Positions')
    plt.legend(loc='best')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()


# In[6]:

#plotting portfolio performance over time with positions
def profit(portfolio,close_price):
    
    data=copy.deepcopy(portfolio)
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    data['asset'].plot(label='Total Asset',color='#58668b')
    
    ax.plot(data.loc[data['signals']==1].index, \
            data['asset'][data['signals']==1],marker='^', \
            c='#00b159',linewidth=0,label='LONG',markersize=11, \
            alpha=1)
    ax.plot(data.loc[data['signals']==-1].index, \
            data['asset'][data['signals']==-1],marker='v', \
            c='#ff6f69',linewidth=0,label='SHORT',markersize=11, \
            alpha=1)
    
    plt.title(f'Oil Money Project\n{close_price.upper()} Total Asset')
    plt.legend(loc='best')
    plt.xlabel('Date')
    plt.ylabel('Asset Value')
    plt.show()


# In[7]:


def main():
    
    df=pd.read_csv('brent crude nokjpy.csv')
    signals=signal_generation(df,'brent','nok',oil_money)
    p=portfolio(signals,'nok')
    
    #pandas.at[] is the fastest but it doesnt support datetime index
    #so we have to set datetime index after iteration but before visualization
    signals.set_index('date',inplace=True)
    signals.index=pd.to_datetime(signals.index,format='%m/%d/%Y')
    p.set_index(signals.index,inplace=True)
    
    #we only visualize data point from 387 to 600
    #becuz the visualization of 5 years data could be too messy
    plot(signals.iloc[387:600],'nok')
    profit(p.iloc[387:600],'nok')
    

if __name__ == '__main__':
    main()

