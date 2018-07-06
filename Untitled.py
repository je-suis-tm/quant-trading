
# coding: utf-8

# In[131]:


#https://en.wikipedia.org/wiki/Parabolic_SAR
#https://www.box.com/s/gbtrjuoktgyag56j6lv0

import matplotlib.pyplot as plt
import numpy as np
import fix_yahoo_finance as yf
import pandas as pd


# In[127]:


stdate=('2016-01-01')
eddate=('2018-01-01')
ticker=('EA')
slicer=450
df=yf.download(ticker,start=stdate,end=eddate)


# In[149]:

def parabolic_sar(new):
    
    initial_af=0.02
    step_af=0.02
    end_af=0.2
    
    
    new['trend']=0
    new['sar']=0.0
    new['real sar']=0.0
    new['ep']=0.0
    new['af']=0.0


    new['trend'][1]=1 if new['Close'][1]>new['Close'][0] else -1
    new['sar'][1]=new['High'][0] if new['trend'][1]>0 else new['Low'][0]
    new.set_value(1,'real sar',new['sar'][1])
    new['ep'][1]=new['High'][1] if new['trend'][1]>0 else new['Low'][1]
    new['af'][1]=initial_af


    for i in range(2,len(new)):
        
        temp=new['sar'][i-1]+new['af'][i-1]*(new['ep'][i-1]-new['sar'][i-1])
        if new['trend'][i-1]<0:
            new.set_value(i,'sar',max(temp,new['High'][i-1],new['High'][i-2]))
            temp=1 if new['sar'][i]<new['High'][i] else new['trend'][i-1]-1
        else:
            new.set_value(i,'sar',min(temp,new['Low'][i-1],new['Low'][i-2]))
            temp=-1 if new['sar'][i]>new['Low'][i] else new['trend'][i-1]+1
        new.set_value(i,'trend',temp)
    
        
        if new['trend'][i]<0:
            temp=min(new['Low'][i],new['ep'][i-1]) if new['trend'][i]!=-1 else new['Low'][i]
        else:
            temp=max(new['High'][i],new['ep'][i-1]) if new['trend'][i]!=1 else new['High'][i]
        new.set_value(i,'ep',temp)
    
    
        if np.abs(new['trend'][i])==1:
            temp=new['ep'][i-1]
            new.set_value(i,'af',initial_af)
        else:
            temp=new['sar'][i]
            if new['ep'][i]==new['ep'][i-1]:
                new.set_value(i,'af',new['af'][i-1])
            else:
                new.set_value(i,'af',min(end_af,new['af'][i-1]+step_af))
        new.set_value(i,'real sar',temp)
       
        
    return new


# In[158]:
def signal_generation(df,method):
    
        new=method(df)

        new['positions'],new['signals']=0,0
        new['positions']=np.where(new['real sar']<new['Close'],1,0)
        new['signals']=new['positions'].diff()
        
        return new






# In[164]:

def plot(new,ticker):
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    new['Close'].plot(lw=3,label='%s'%ticker)
    new['real sar'].plot(linestyle=':',label='Parabolic SAR',color='k')
    ax.plot(new.loc[new['signals']==1].index,new['Close'][new['signals']==1],marker='^',color='g',label='LONG',lw=0,markersize=10)
    ax.plot(new.loc[new['signals']==-1].index,new['Close'][new['signals']==-1],marker='v',color='r',label='SHORT',lw=0,markersize=10)
    
    plt.legend()
    plt.grid(True)
    plt.title('Parabolic SAR')
    plt.ylabel('%s'%ticker)
    plt.show()


#
del df['Adj Close']
del df['Volume']

df.reset_index(inplace=True)

new=signal_generation(df,parabolic_sar)

new.set_index(new['Date'],inplace=True)
new=new[slicer:]

plot(new,ticker)