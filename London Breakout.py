
# coding: utf-8

# In[2]:


import os
os.chdir('d:')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[3]:



df=pd.read_csv('eurgbp.csv')
a=np.array(df['price'])

threshold=[]
risky=0.01
londonopen=50
i=0
start=float(0)
signals=pd.DataFrame(index=pd.to_datetime(df['date']))

signals['signals']=0
signals['cumsum']=0
signals['price']=a
signals['date']=signals.index



# In[4]:


while i<=len(signals['date'])-1:
    if signals['date'][i].hour==2:
        threshold.append(signals['price'][i])
    
    elif signals['date'][i].hour==3 and signals['date'][i].minute==0:
        upper=max(threshold)
        lower=min(threshold)
        threshold=[]
    
    elif signals['date'][i].hour==3 and signals['date'][i].minute<londonopen:
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


# In[6]:


fig=plt.figure()

ax=fig.add_subplot(111)

signals['price'].plot(label='price')
ax.plot(signals.loc[signals['signals']==1].index,signals['price'][signals['signals']==1],lw=0,marker='^',c='g',label='LONG')
ax.plot(signals.loc[signals['signals']==-1].index,signals['price'][signals['signals']==-1],lw=0,marker='v',c='r',label='SHORT')
plt.xlabel('date')
plt.ylabel('eurgbp')
plt.legend(loc='best')
plt.title('London Breakout')
plt.grid(True)
plt.show()

