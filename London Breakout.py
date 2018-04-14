
# coding: utf-8

# In[1]:


import os
os.chdir('d:')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[8]:



df=pd.read_csv('eurgbp.csv')
a=np.array(df['price'])

threshold=[]
risky=0.01
londonopen=30
i=0
start=float(0)
signals=pd.DataFrame(index=pd.to_datetime(df['date']))

signals['signals']=0
signals['cumsum']=0
signals['price']=a
signals['date']=signals.index
signals['upper']=0.0
signals['lower']=0.0



# In[9]:


while i<=len(signals['date'])-1:
    if signals['date'][i].hour==2:
        threshold.append(signals['price'][i])
    
    elif signals['date'][i].hour==3 and signals['date'][i].minute==0:
        upper=max(threshold)
        lower=min(threshold)
        signals['upper'][i]=upper
        signals['lower'][i]=lower
        threshold=[]
    
    elif signals['date'][i].hour==3 and signals['date'][i].minute<londonopen:
        
        signals['upper'][i]=upper
        signals['lower'][i]=lower
        
        if signals['price'][i]-upper>0:
            signals['signals'][i]=1
            signals['cumsum']=signals['signals'].cumsum()
            if signals['price'][i]-upper>risky:
                signals['signals'][i]=0
            elif signals['cumsum'][i]>1:
                signals['signals'][i]=0
            else:
                start=df['price'][i]
                
                
            
            
        if signals['price'][i]-lower<0:
            signals['signals'][i]=-1
            signals['cumsum']=signals['signals'].cumsum()
            if df['price'][i]-lower<risky:
                signals['signals'][i]=0
            elif signals['cumsum'][i]<-1:
                signals['signals'][i]=0
            else:
                start=signals['price'][i]
        
        
    
    elif signals['date'][i].hour==12:
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][i]=-signals['cumsum'][i]
        
        
    else:
        signals['cumsum']=signals['signals'].cumsum()
        if signals['cumsum'][i]!=0:
            if signals['price'][i]>start+risky/2:
                signals['signals'][i]=-signals['cumsum'][i]
            if df['price'][i]<start-risky/2:
                signals['signals'][i]=-signals['cumsum'][i]
        
            
        
    i+=1


# In[204]:

temp=[]

for j in signals.loc[signals['signals']!=0].index:
    temp.append(str(j.year)+'-'+str(j.month)+'-'+str(j.day))

f='%s 00:00:00'%(min(temp))
l='%s 14:00:00'%(max(temp))
new=signals[f:l]

fig=plt.figure()
ax=fig.add_subplot(111)
new['price'].plot(label='EURGBP')
ax.plot(new.loc[new['signals']==1].index,new['price'][new['signals']==1],lw=0,marker='^',c='g',label='LONG')
ax.plot(new.loc[new['signals']==-1].index,new['price'][new['signals']==-1],lw=0,marker='v',c='r',label='SHORT')

plt.legend(loc='best')
plt.title('London Breakout')
for k in set(temp):
    plt.axvline('%s 03:00:00'%(k),linestyle=':',c='k')
plt.ylabel('price')    
plt.grid(True)
plt.show()


# In[212]:


f='%s 02:50:00'%(min(temp))
l='%s 03:30:00'%(min(temp))
news=signals[f:l]

fig=plt.figure()

bx=fig.add_subplot(111)
plt.grid(True)
plt.ylabel('EURGBP')
plt.xlabel('time interval')
plt.title('Threshold')
plt.xticks([])
bx.plot(news.loc[news['signals']==1].index,news['price'][news['signals']==1],lw=0,marker='^',markersize=10,c='g',label='LONG')
bx.plot(news.loc[news['signals']==-1].index,news['price'][news['signals']==-1],lw=0,marker='v',markersize=10,c='r',label='SHORT')
bx.plot(news.loc[news['upper']!=0].index,news['upper'][news['upper']!=0],lw=0,marker='.',markersize=7,c='#BC8F8F',label='upper threshold')
bx.plot(news.loc[news['lower']!=0].index,news['lower'][news['lower']!=0],lw=0,marker='.',markersize=5,c='#FF4500',label='lower threshold')
bx.plot(news['price'],label='EURGBP')

plt.legend(loc='best')
plt.show()




