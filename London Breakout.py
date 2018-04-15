
# coding: utf-8

# In[1]:

#this is to London, the best city in the world
#i was a Londoner, proud of being Londoner, how i love the city!
#to St Paul, Tate Modern, Millennium Bridge and so much more!

#okay, lets get down to business
#the idea of london break out strategy is to take advantage of fx trading hour
#basically fx trading is 24 hour non stop for weekdays
#u got tokyo, when tokyo closes, u got london
#in the afternoon, u got new york, when new york closes, its sydney
#and several hours later, tokyo starts again
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
#please note that this website uses new york time zone utc-5
#for non summer daylight saving time
#london market starts at gmt 8 am
#which is est 3 am
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
#cumsum is the cumulated sum of signals
#later we would use it to control our positions
signals['cumsum']=0
signals['price']=a
signals['date']=signals.index
#upper and lower are lists that store our thresholds
signals['upper']=0.0
signals['lower']=0.0



# In[9]:
#this is the core part
#the time complexity for this part is extremely high
#as there are too many constraints
#if u have a better idea to optimize it
#plz let me know

#it doesnt matter we are using while or for function
#we just have to do a traversal on elements in historical datasets
while i<=len(signals['date'])-1:
    #like i have mentioned before
    #my datasets use eastern standard time
    #so est 2am is the last hour of tokyo market
    #we try to append all the price into the list called threshold
    if signals['date'][i].hour==2:
        threshold.append(signals['price'][i])
    
    #est 3am which is gmt 8am
    #thats when london market starts
    #good morning monument and canary wharf!
    #right at this moment
    #we get max and min of the price of tokyo trading hour
    #i set up the threshold as the way it is
    #alternatively, we can put 10 basis points above and below thresholds
    #we also use upper and lower list to keep track of our thresholds
    #and now we clear the list called threshold
    elif signals['date'][i].hour==3 and signals['date'][i].minute==0:
        upper=max(threshold)
        lower=min(threshold)
        signals['upper'][i]=upper
        signals['lower'][i]=lower
        threshold=[]
    
    #prior to 30 minutes i have mentioned before
    #as long as its under 30 minutes after market opening
    #signals will be generated once conditions are met
    #this is a risky way
    #alternatively, we can set the signal generation time at a fixed point
    #when its gmt 8 30 am, we check the conditions to see if there is any signal
    #in that case, second part of if function would be
    #signals['date'][i].minute==londonopen
    elif signals['date'][i].hour==3 and signals['date'][i].minute<londonopen:
        #again, we wanna keep track of thresholds during signal generation periods
        signals['upper'][i]=upper
        signals['lower'][i]=lower
        
        
        #this is the condition of signals generation
        #when the price is above upper threshold
        #we set signals to 1 which implies long
        if signals['price'][i]-upper>0:
            signals['signals'][i]=1
            #we use cumsum to check the cumulated sum of signals
            #we wanna make sure that
            #only the first price above upper threshold triggers the signal
            #also, if it goes skyrocketing
            #say 200 basis points above, which is 100 above my risk tolerance
            #we set it as a false alarm
            signals['cumsum']=signals['signals'].cumsum()
            if signals['price'][i]-upper>risky:
                signals['signals'][i]=0
            elif signals['cumsum'][i]>1:
                signals['signals'][i]=0
            else:
                #we also need to store the price when we execute a trade
                #its for stop loss calculation
                start=df['price'][i]
                
                
            
        #vice versa    
        if signals['price'][i]-lower<0:
            signals['signals'][i]=-1
            signals['cumsum']=signals['signals'].cumsum()
            if df['price'][i]-lower<risky:
                signals['signals'][i]=0
            elif signals['cumsum'][i]<-1:
                signals['signals'][i]=0
            else:
                start=signals['price'][i]
        
        
    #when its gmt 5 pm, london market closes
    #we use cumsum to see if there is any position left open
    #we take -cumsum as a signal
    #if there is no open position, -0 is still 0
    elif signals['date'][i].hour==12:
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][i]=-signals['cumsum'][i]
        
    #during london trading hour after opening but before closing
    #we still use cumsum to check our open positions
    #if there is any open position
    #we set our consition at original executed price +/- half of the risk interval
    #when it goes above or below my risk tolerance
    #i clear positions to claim profit or loss
    else:
        signals['cumsum']=signals['signals'].cumsum()
        if signals['cumsum'][i]!=0:
            if signals['price'][i]>start+risky/2:
                signals['signals'][i]=-signals['cumsum'][i]
            if df['price'][i]<start-risky/2:
                signals['signals'][i]=-signals['cumsum'][i]
        
            
        
    i+=1


# In[204]:
#after signals generations
#lets visualize the result
#firstly, i add a new list called temp
#it stores the information when trades have been executed 
temp=[]
#i use a condition slicing on when signals doesnt equal to zero
#that is when trades are executed
#i get the datetime index and format it
#append it to a list called temp
for j in signals.loc[signals['signals']!=0].index:
    temp.append(str(j.year)+'-'+str(j.month)+'-'+str(j.day))


#this is just another slicing
#i take 0am which is before london market opening
#and 2pm which is after london market opening
#i get min and max from list called temp
#then i slice on dataframe called temp
#becuz i dont wanna plot the whole historical datasets
#it would be too messy
#i just wanna see those days when trades occur
f='%s 00:00:00'%(min(temp))
l='%s 14:00:00'%(max(temp))
new=signals[f:l]

#the first plot is eurgbp average price with LONG/SHORT positions
fig=plt.figure()
ax=fig.add_subplot(111)
new['price'].plot(label='EURGBP')
ax.plot(new.loc[new['signals']==1].index,new['price'][new['signals']==1],lw=0,marker='^',c='g',label='LONG')
ax.plot(new.loc[new['signals']==-1].index,new['price'][new['signals']==-1],lw=0,marker='v',c='r',label='SHORT')
plt.legend(loc='best')
plt.title('London Breakout')
#this is the part where i add some vertical line to indicate specific dates
#i use set function to get list called temp without any duplicates
for k in set(temp):
    plt.axvline('%s 03:00:00'%(k),linestyle=':',c='k')
plt.ylabel('price')    
plt.grid(True)
plt.show()


# In[212]:

#this is almost the same process of previous slicing
#except i only look at the first trade and break it down into 110 minutes
#i wanna observe how the price goes beyond the threshold
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
#i only need to plot non zero thresholds
#zero is the value outta market opening period (30 minutes in this case)
bx.plot(news.loc[news['upper']!=0].index,news['upper'][news['upper']!=0],lw=0,marker='.',markersize=7,c='#BC8F8F',label='upper threshold')
bx.plot(news.loc[news['lower']!=0].index,news['lower'][news['lower']!=0],lw=0,marker='.',markersize=5,c='#FF4500',label='lower threshold')
bx.plot(news['price'],label='EURGBP')

plt.legend(loc='best')
plt.show()




