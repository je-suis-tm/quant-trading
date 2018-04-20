
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf


# In[2]:


ma1=5
ma2=34

stdate=input('start date in format yyyy-mm-dd:')
eddate=input('end date in format yyyy-mm-dd:')
ticker=input('ticker:')
#slicing the downloaded dataset, if the dataset is too large, backtesting plot would look messy
st=int(input('slicing:'))


# In[3]:


df=yf.download(ticker,start=stdate,end=eddate)
signals=pd.DataFrame(df)


# In[46]:


signals['macd ma1']=pd.ewma(signals['Close'],span=ma1)
signals['macd ma2']=pd.ewma(signals['Close'],span=ma2)
signals['macd signals']=0
signals['macd signals'][ma1:]=np.where(signals['macd ma1'][ma1:]>=signals['macd ma2'][ma1:],1,0)
signals['macd trade']=signals['macd signals'].diff()
signals['macd oscillator']=signals['macd ma1']-signals['macd ma2']


# In[47]:


signals['awesome ma1'],signals['awesome ma2']=0,0
signals['awesome ma1']=((signals['High']+signals['Low'])/2).rolling(window=5).mean()
signals['awesome ma2']=((signals['High']+signals['Low'])/2).rolling(window=34).mean()
signals['awesome signals']=0
signals['awesome oscillator']=signals['awesome ma1']-signals['awesome ma2']  
signals['awesome signals'][34:]=np.where(signals['awesome ma1'][34:]>=signals['awesome ma2'][34:],1,0)
signals['awesome trade']=signals['awesome signals'].diff()


# In[88]:



new=signals[st:]


fig=plt.figure()
ax=fig.add_subplot(211)
new['Close'].plot(label=ticker)
ax.plot(new.loc[new['awesome trade']==1].index,new['Close'][new['awesome trade']==1],label='AWESOME LONG',lw=0,marker='^',c='g')
ax.plot(new.loc[new['awesome trade']==-1].index,new['Close'][new['awesome trade']==-1],label='AWESOME SHORT',lw=0,marker='v',c='r')
plt.legend(loc='best')
plt.grid(True)
plt.title('Positions')
bx=fig.add_subplot(212,sharex=ax)
new['Close'].plot(label=ticker)
bx.plot(new.loc[new['macd trade']==1].index,new['Close'][new['macd trade']==1],label='MACD LONG',lw=0,marker='^',c='g')
bx.plot(new.loc[new['macd trade']==-1].index,new['Close'][new['macd trade']==-1],label='MACD SHORT',lw=0,marker='v',c='r')
plt.legend(loc='best')
plt.grid(True)
plt.show()


fig=plt.figure()
cx=fig.add_subplot(211)
c=np.where(new['Open']>new['Close'],'r','g')
cx.bar(range(len(new)),new['awesome oscillator'],color=c,label='awesome oscillator')
plt.grid(True)
plt.legend(loc='best')
plt.title('Oscillator')
dx=fig.add_subplot(212,sharex=cx)
new['macd oscillator'].plot(kind='bar',label='macd oscillator')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('')
plt.xticks([])
plt.show()



fig=plt.figure()
ex=fig.add_subplot(211)
new['awesome ma1'].plot(label='awesome ma1')
new['awesome ma2'].plot(label='awesome ma2',linestyle=':')
plt.legend(loc='best')
plt.grid(True)
plt.xticks([])
plt.xlabel('')
plt.title('Moving Average')
fig=plt.figure()
fx=fig.add_subplot(212,sharex=bx)
new['macd ma1'].plot(label='macd ma1')
new['macd ma2'].plot(label='macd ma2',linestyle=':')
plt.legend(loc='best')
plt.grid(True)
plt.show()

