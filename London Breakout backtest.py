# coding: utf-8

# In[1]:

#this is to London, the greatest city in the world
#i was a Londoner, proud of being Londoner, how i love the city!
#to St Paul, Tate Modern, Millennium Bridge and so much more!

#okay, lets get down to business
#the idea of london break out strategy is to take advantage of fx trading hour
#basically fx trading is 24 hour non stop for weekdays
#u got tokyo, before tokyo closes, u got london
#in the afternoon, u got new york, when new york closes, its sydney
#and several hours later, tokyo starts again
#however, among these three major players
#london is where the majority trades are executed
#not sure if it will stay the same after brexit actually takes place
#what we intend to do is look at the last trading hour before london starts
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
#please note that this website uses new york time zone utc -5
#for non summer daylight saving time
#london market starts at gmt 8 am
#which is est 3 am
#daylight saving time is another story
#what a stupid idea it is
import os
os.chdir('d:/')
import matplotlib.pyplot as plt
import pandas as pd

# In[2]:

def london_breakout(df):
    
    df['signals']=0

    #cumsum is the cumulated sum of signals
    #later we would use it to control our positions
    df['cumsum']=0

    #upper and lower are our thresholds
    df['upper']=0.0
    df['lower']=0.0

    return df


def signal_generation(df,method):
    
    #tokyo_price is a list to store average price of
    #the last trading hour of tokyo market
    #we use max, min to define the real threshold later
    tokyo_price=[]

    #risky_stop is a parameter set by us
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
    risky_stop=0.01

    #this is another parameter set by us
    #it is about how long opening volatility would wear off
    #for me, 30 minutes after the market opening is the boundary
    #as long as its under 30 minutes after the market opening
    #if the price reaches threshold level, i will trade on signals
    open_minutes=30

    #this is the price when we execute a trade
    #we need to save it to set up the stop loss
    executed_price=float(0)
    
    signals=method(df)
    signals['date']=pd.to_datetime(signals['date'])
    
    #this is the core part
    #the time complexity for this part is extremely high
    #as there are too many constraints
    #if u have a better idea to optimize it
    #plz let me know

    for i in range(len(signals)):
        
        #as mentioned before
        #the dataset use eastern standard time
        #so est 2am is the last hour before london starts
        #we try to append all the price into the list called threshold
        if signals['date'][i].hour==2:
            tokyo_price.append(signals['price'][i])
            
        #est 3am which is gmt 8am
        #thats when london market starts
        #good morning city of london and canary wharf!
        #right at this moment
        #we get max and min of the price of tokyo trading hour
        #we set up the threshold as the way it is
        #alternatively, we can put 10 basis points above and below thresholds
        #we also use upper and lower list to keep track of our thresholds
        #and now we clear the list called threshold
        elif signals['date'][i].hour==3 and signals['date'][i].minute==0:

            upper=max(tokyo_price)
            lower=min(tokyo_price)

            signals.at[i,'upper']=upper
            signals.at[i,'lower']=lower

            tokyo_price=[]
            
        #prior to 30 minutes i have mentioned before
        #as long as its under 30 minutes after market opening
        #signals will be generated once conditions are met
        #this is a relatively risky way
        #alternatively, we can set the signal generation time at a fixed point
        #when its gmt 8 30 am, we check the conditions to see if there is any signal
        elif signals['date'][i].hour==3 and signals['date'][i].minute<open_minutes:

            #again, we wanna keep track of thresholds during signal generation periods
            signals.at[i,'upper']=upper
            signals.at[i,'lower']=lower
            
            #this is the condition of signals generation
            #when the price is above upper threshold
            #we set signals to 1 which implies long
            if signals['price'][i]-upper>0:
                signals.at[i,'signals']=1

                #we use cumsum to check the cumulated sum of signals
                #we wanna make sure that
                #only the first price above upper threshold triggers the signal
                #also, if it goes skyrocketing
                #say 200 basis points above, which is 100 above our risk tolerance
                #we set it as a false alarm
                signals['cumsum']=signals['signals'].cumsum()

                if signals['price'][i]-upper>risky_stop:
                    signals.at[i,'signals']=0

                elif signals['cumsum'][i]>1:
                    signals.at[i,'signals']=0

                else:

                    #we also need to store the price when we execute a trade
                    #its for stop loss calculation
                    executed_price=signals['price'][i]

            #vice versa    
            if signals['price'][i]-lower<0:
                signals.at[i,'signals']=-1

                signals['cumsum']=signals['signals'].cumsum()

                if lower-signals['price'][i]>risky_stop:
                    signals.at[i,'signals']=0

                elif signals['cumsum'][i]<-1:
                    signals.at[i,'signals']=0

                else:
                    executed_price=signals['price'][i]
                    
        #when its gmt 5 pm, london market closes
        #we use cumsum to see if there is any position left open
        #we take -cumsum as a signal
        #if there is no open position, -0 is still 0
        elif signals['date'][i].hour==12:
            signals['cumsum']=signals['signals'].cumsum()
            signals.at[i,'signals']=-signals['cumsum'][i]
            
        #during london trading hour after opening but before closing
        #we still use cumsum to check our open positions
        #if there is any open position
        #we set our condition at original executed price +/- half of the risk interval
        #when it goes above or below our risk tolerance
        #we clear positions to claim profit or loss
        else:
            signals['cumsum']=signals['signals'].cumsum()
            
            if signals['cumsum'][i]!=0:
                if signals['price'][i]>executed_price+risky_stop/2:
                    signals.at[i,'signals']=-signals['cumsum'][i]
                    
                if signals['price'][i]<executed_price-risky_stop/2:
                    signals.at[i,'signals']=-signals['cumsum'][i]
    
    return signals



def plot(new):
    
    #the first plot is price with LONG/SHORT positions
    fig=plt.figure()
    ax=fig.add_subplot(111)

    new['price'].plot(label='price')

    ax.plot(new.loc[new['signals']==1].index,new['price'][new['signals']==1],lw=0,marker='^',c='g',label='LONG')
    ax.plot(new.loc[new['signals']==-1].index,new['price'][new['signals']==-1],lw=0,marker='v',c='r',label='SHORT')
      
    #this is the part where i add some vertical line to indicate market beginning and ending
    date=new.index[0].strftime('%Y-%m-%d')
    plt.axvline('%s 03:00:00'%(date),linestyle=':',c='k')
    plt.axvline('%s 12:00:00'%(date),linestyle=':',c='k')


    plt.legend(loc='best')
    plt.title('London Breakout')
    plt.ylabel('price')
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()


    #lets look at the market opening and break it down into 110 minutes
    #we wanna observe how the price goes beyond the threshold

    f='%s 02:50:00'%(date)
    l='%s 03:30:00'%(date)
    news=signals[f:l]
    fig=plt.figure()
    bx=fig.add_subplot(111)

    bx.plot(news.loc[news['signals']==1].index,news['price'][news['signals']==1],lw=0,marker='^',markersize=10,c='g',label='LONG')
    bx.plot(news.loc[news['signals']==-1].index,news['price'][news['signals']==-1],lw=0,marker='v',markersize=10,c='r',label='SHORT')

    #i only need to plot non zero thresholds
    #zero is the value outta market opening period 
    bx.plot(news.loc[news['upper']!=0].index,news['upper'][news['upper']!=0],lw=0,marker='.',markersize=7,c='#BC8F8F',label='upper threshold')
    bx.plot(news.loc[news['lower']!=0].index,news['lower'][news['lower']!=0],lw=0,marker='.',markersize=5,c='#FF4500',label='lower threshold')
    bx.plot(news['price'],label='price')


    plt.grid(True)
    plt.ylabel('price')
    plt.xlabel('time interval')
    plt.xticks([])
    plt.title('%s Market Opening'%date)
    plt.legend(loc='best')
    plt.show()
    
    
# In[3]:
def main():
    
    df=pd.read_csv('gbpusd.csv')

    signals=signal_generation(df,london_breakout)

    new=signals
    new.set_index(pd.to_datetime(signals['date']),inplace=True)
    date=new.index[0].strftime('%Y-%m-%d')
    new=new['%s'%date]

    plot(new)

#how to calculate stats could be found from my other code called Heikin-Ashi
# https://github.com/je-suis-tm/quant-trading/blob/master/heikin%20ashi%20backtest.py

if __name__ == '__main__':
    main()
