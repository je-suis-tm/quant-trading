
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy as np


# In[2]:


os.chdir('d:/')


# In[3]:


def bollinger_bands(df):
    
    data=copy.deepcopy(df)
    data['std']=data['price'].rolling(window=20,min_periods=20).std()
    data['mid band']=data['price'].rolling(window=20,min_periods=20).mean()
    data['upper band']=data['mid band']+2*data['std']
    data['lower band']=data['mid band']-2*data['std']
    
    return data


# In[4]:


def signal_generation(data,method):
    
    period=75
    alpha=0.0001
    beta=0.0001
    
    df=method(data)
    df['signals']=0
    df['cumsum']=0
    df['coordinates']=''
    
    for i in range(period,len(df)):
        
        moveon=False
        threshold=0.0
        
        #bottom w pattern recognition
        #condition 4
        if (df['price'][i]>df['upper band'][i]) and         (df['cumsum'][i]==0):
            
            for j in range(i,i-period,-1):                
                #condition 2
                if (np.abs(df['mid band'][j]-df['price'][j])<alpha) and                 (np.abs(df['mid band'][j]-df['upper band'][i])<alpha):
                    moveon=True
                    break
            
            if moveon==True:
                moveon=False
                for k in range(j,i-period,-1):
                    #condition 1
                    if (np.abs(df['lower band'][k]-df['price'][k])<alpha):
                        threshold=df['price'][k]
                        moveon=True
                        break
                        
            if moveon==True:
                moveon=False
                for l in range(k,i-period,-1):
                    #this one is for plotting w shape
                    if (df['mid band'][l]<df['price'][l]):
                        moveon=True
                        break
                    
            if moveon==True:
                moveon=False        
                for m in range(i,j,-1):
                    #condition 3
                    if (df['price'][m]-df['lower band'][m]<alpha) and                     (df['price'][m]>df['lower band'][m]) and                     (df['price'][m]<threshold):
                        df.set_value(i,'signals',1)
                        df.set_value(i,'coordinates','%s,%s,%s,%s,%s'%(l,k,j,m,i))
                        df['cumsum']=df['signals'].cumsum()
                        moveon=True
                        break
        
        #clear our positions when there is contraction on bollinger bands
        if (df['cumsum'][i]!=0) and         (df['std'][i]<beta) and         (moveon==False):
            df.set_value(i,'signals',-1)
            df['cumsum']=df['signals'].cumsum()
            
    return df


# In[5]:


def plot(new):
    
    a,b=list(new[new['signals']!=0].iloc[:2].index)
    a,b=(2199,2301)
    
    newbie=new[a-85:b+30]
    newbie.set_index(pd.to_datetime(newbie['date'],format='%Y-%m-%d %H:%M:%S'),inplace=True)

    
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)

    ax.plot(newbie['price'],label='price')
    ax.fill_between(newbie.index,newbie['lower band'],newbie['upper band'],alpha=0.2,color='#45ADA8')
    ax.plot(newbie['mid band'],linestyle='--',label='moving average',c='#132226')
    ax.plot(newbie['price'][newbie['signals']==1],marker='^',markersize=12,            lw=0,c='g',label='LONG')
    ax.plot(newbie['price'][newbie['signals']==-1],marker='v',markersize=12,            lw=0,c='r',label='SHORT')
    
    temp=newbie['coordinates'][newbie['signals']==1]
    indexlist=list(map(int,temp[temp.index[0]].split(',')))
    ax.plot(newbie['price'][pd.to_datetime(new['date'].iloc[indexlist])],            lw=5,alpha=0.7,c='#FE4365',label='double bottom pattern')
    
    
    plt.text((newbie.loc[newbie['signals']==1].index[0]),             newbie['lower band'][newbie['signals']==1],'Expansion',fontsize=15,color='563838')
    plt.text((newbie.loc[newbie['signals']==-1].index[0]),             newbie['lower band'][newbie['signals']==-1],'Contraction',fontsize=15,color='563838')
    
    plt.legend(loc='best')
    plt.title('Bollinger Bands Pattern Recognition')
    plt.ylabel('price')
    plt.grid(True)
    plt.show()


# In[6]:


df=pd.read_csv('gbpusd.csv')


# In[7]:


signals=signal_generation(df,bollinger_bands)


# In[8]:


new=copy.deepcopy(signals)
plot(new)

