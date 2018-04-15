
# coding: utf-8

# In[1]:

#this is to London, the best city in the world
#i was a Londoner, proud of being Londoner, how i love the city!
#to St Paul, Tate Modern, Millennium Bridge and so much more!

#okay, lets get down to business
#the idea of london break out strategy is to take advantage of fx trading hour
#basically fx trading is 24 hour non stop for weekdays
#u got tokyo, when tokyo closes, u got london
#in the afternoon, u got new york, when new york closes, its tokyo again
#however, among these three major players
#london is where the majority trades are executed
#not sure if it will stay the same after brexit actually takes place
#what we intend to do is look at the last trading hour of tokyo
#we set up our thresholds based on that hours high and low
#when london market opens, we examine the first 30 minutes
#if it goes way above or below thresholds
#we long or short certain currency pairs
#and we clear our positions based on target and stop loss we set
#if they havent reach the trigger condition by the end of trading hour
#we exit our trades and close all positions

#it sounds easy in practise
#just a simple prediction of london fx market based on tokyo market
#but the code of london breakout is extremely time consuming
#first, we need to get one minute frequency dataset for backtest
#i would recommend this website
# http://www.histdata.com/download-free-forex-data/?/excel/1-minute-bar-quotes
#we can get as many as free datasets of various currency pairs we want
#before our backtesting, we should cleanse the raw data
#what we get from the website is one minute frequency bid-ask price
#i take the average of em and add a header called price
#i save it on local disk then read it via python
import os
os.chdir('d:')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[8]:
df=pd.read_csv('eurgbp.csv')


#as i have mentioned before
#we add a header called price
#the reason of using numpy array on price is that
#we are gonna use time series in pandas for backtesting
#if we dont assign an extra array to store price
#we might have some index collision 
#as eurgbp.csv has a discrete number index
a=np.array(df['price'])
#threshold is a list to store average price of
#the last trading hour of tokyo market
#we use max, min to define the real threshold later
threshold=[]
#risky is a parameter set by us
#it is to reduce the risk exposure to volatility
#i am using 100 basis points
#for instance, we have defined our upper and lower thresholds
#however, when london market opens
#the price goes skyrocketing 
#say 200 basis points above upper threshold
#i personally wouldnt get in the market as its too risky
#also, my stop loss and target is 50 basis points
#just half of my risk interval
#i will use this variable for later stop loss set up
risky=0.01
#london open is anoher parameter set by us
#it is about how long opening volatility would wear off
#for me, 30 minutes after the market opening is the boundary
#as long as its under 30 minutes after the market opening
#if the price reaches threshold level, i will trade on signals
londonopen=30
#i is the iteration of all elements in our historical data
i=0
#start is the price when we execute a trade
#we need to save it to set up the stop loss
start=float(0)



#we use pandas to datetime to set up datetime index
#so the price would become time series
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




