
# coding: utf-8

# In[1]:


import statsmodels.api as sm
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('d:/')


# In[2]:


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


def signal_generation(dataset,x,y,method, \
                      holding_threshold=10, \
                      stop=0.5,rsquared_threshold=0.7, \
                      train_len=50):
    
    df=method(dataset)

    holding=0
    trained=False
    counter=0
    

    for i in range(train_len,len(df)):
    
        if holding!=0:
            if counter>holding_threshold:
                df.at[i,'signals']=-holding            
                holding=0
                trained=False
                counter=0
            
                df.at[i:,'pos2 sigma']=df['forecast']
                df.at[i:,'neg2 sigma']=df['forecast']
                df.at[i:,'pos1 sigma']=df['forecast']
                df.at[i:,'neg1 sigma']=df['forecast']
                continue
                
            if np.abs( \
                      df[y].iloc[i]-df[y][df['signals']!=0].iloc[-1] \
                      )>=stop:
                df.at[i,'signals']=-holding        
                holding=0
                trained=False
                counter=0
            
                df.at[i:,'pos2 sigma']=df['forecast']
                df.at[i:,'neg2 sigma']=df['forecast']
                df.at[i:,'pos1 sigma']=df['forecast']
                df.at[i:,'neg1 sigma']=df['forecast']
                continue
        
            counter+=1
    
        else:
            if not trained:
                X=sm.add_constant(df[x].iloc[i-train_len:i])
                Y=df[y].iloc[i-train_len:i]
                m=sm.OLS(Y,X).fit()
                if m.rsquared>rsquared_threshold:
                    trained=True
                    sigma=np.std(Y-m.predict(X))
                    
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
        
            if trained:
                if df[y].iloc[i]>df['pos2 sigma'].iloc[i]:
                    df.at[i,'signals']=1
                    holding=1
                if df[y].iloc[i]<df['neg2 sigma'].iloc[i]:
                    df.at[i,'signals']=-1
                    holding=-1  

                    
    return df
    


# In[4]:


def portfolio(signals,close_price,capital0=5000,positions=250):   

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
    signals.set_index('date',inplace=True)
    signals.index=pd.to_datetime(signals.index,format='%m/%d/%Y')
    p.set_index(signals.index,inplace=True)
    plot(signals.iloc[387:600],'nok')
    profit(p.iloc[387:600],'nok')
    

if __name__ == '__main__':
    main()

