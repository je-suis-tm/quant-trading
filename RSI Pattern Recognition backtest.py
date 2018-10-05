# coding: utf-8

# In[1]:

#relative strength index(rsi) is another popular indicator for technical analysis
#actually i believe its kinda bull shit
#normally i read stuff on trading view wiki
#its not like i work there and try to promote it
#trading view wiki is a very detailed encyclopedia for different indicators
#plz refer to the following link for more details
# https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)

#on trading view wiki, there are a couple of strategies to use rsi
#the simplest one is overbought/oversold
#that is what this script is about
#we just set upper/lower boundaries capped at 30/70 for rsi
#if rsi exceeds the bound, we bet the stock would go under price correction

#another one is called divergence
#rsi goes up and price actually goes down
#the inventor of rsi called wilder believes bearish rsi divergence creates a selling opportunity 
#but his protege cardwell believes bearish divergence only occurs in a bullish trend
#so their ideas basically contradict to each other
#i would undoubtedly give up on this bs divergence strategy

#the last one is called failure swing
#its kinda like a double bottom pattern in price itself
#except this strategy is a pattern recognition on rsi
#since i have written bottom w pattern for bollinger bands
#i would not do it here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf


# In[2]:

#smoothed moving average
#for details plz refer to wikipedia
# https://en.wikipedia.org/wiki/Moving_average#Modified_moving_average
def smma(series,n):
    
    output=[series[0]]
    
    for i in range(1,len(series)):
        temp=output[-1]*(n-1)+series[i]
        output.append(temp/n)
        
    return output


# In[3]:

#calculating rsi is very simple
#except there are several versions of moving average for rsi
#simple moving average, exponentially weighted moving average, etc
#in this script, we use smoothed moving average(the authentic way)
def rsi(data,n=14):
    
    delta=data.diff().dropna()
    
    up=np.where(delta>0,delta,0)
    down=np.where(delta<0,-delta,0)
    
    rs=np.divide(smma(up,n),smma(down,n))
    
    output=100-100/(1+rs)
    
    return output[n-1:]


# In[4]:

#signal generation
#it is really easy
#when rsi goes above 70, we short the stock
#we bet the stock price would fall
#vice versa
def signal_generation(df,method,n=14):
    
    df['rsi']=0.0
    df['rsi'][n:]=method(df['Close'],n=14)
    
    df['positions']=np.select([df['rsi']<30,df['rsi']>70], \
                              [1,-1],default=0)
    df['signals']=df['positions'].diff()
    
    return df[n:]


# In[5]:

#plotting
def plot(new,ticker):
    
    #the first plot is the actual close price with long/short positions
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(211)
    
    new['Close'].plot(label=ticker)
    ax.plot(new.loc[new['signals']==1].index,
            new['Close'][new['signals']==1],
            label='LONG',lw=0,marker='^',c='g')
    ax.plot(new.loc[new['signals']==-1].index,
            new['Close'][new['signals']==-1],
            label='SHORT',lw=0,marker='v',c='r')

    
    plt.legend(loc='best')
    plt.grid(True)
    plt.title('Positions')
    plt.xlabel('Date')
    plt.ylabel('price')
    
    plt.show()
    
    #the second plot is rsi with overbought/oversold interval capped at 30/70
    bx=plt.figure(figsize=(10,10)).add_subplot(212,sharex=ax)
    new['rsi'].plot(label='relative strength index',c='#522e75')
    bx.fill_between(new.index,30,70,alpha=0.5,color='#f22f08')
    
    bx.text(new.index[-45],75,'overbought',color='#594346',size=12.5)
    bx.text(new.index[-45],25,'oversold',color='#594346',size=12.5)
    
    plt.xlabel('Date')
    plt.ylabel('value')
    plt.title('RSI')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


# In[6]:

#pattern recognition
#do u really think i would write such an easy script?
#dont be naive, here is another way of using rsi
#unlike double bottom pattern for bollinger bands
#this is head-shoulder pattern directly on rsi instead of price
#well, it is actually named head and shoulders
#but i refused to do free marketing for the shampoo
#cuz that shampoo doesnt work at all!
#the details of head-shoulder pattern could be found in this link
# https://www.investopedia.com/terms/h/head-shoulders.asp

#any way, this pattern recognition is similar to the one in bollinger bands
#plz refer to bollinger bands for a detailed explanation
# https://github.com/tattooday/quant-trading/blob/master/Bollinger%20Bands%20Pattern%20Recognition%20backtest.py
def pattern_recognition(df,method,lag=14):
    
    df['rsi']=0.0
    df['rsi'][lag:]=method(df['Close'],lag)    
    
    #as usual, period is defined as the horizon for finding the pattern
    period=25    
    
    #delta is the threshold of the difference between two prices
    #if the difference is smaller than delta, we conclude two prices are almost the same
    #we do not expect nodes of shoulder are exactly the same
    #its okay to be slightly different
    #we denote delta as the word slightly
    delta=0.2
    
    #these are the multipliers of delta
    #we wanna make sure there is a large difference between head and shoulders
    #the difference is defined as head/shoulder multiplier*delta
    head=1.1
    shoulder=1.1
    
    df['signals']=0
    df['cumsum']=0
    df['coordinates']=''
    
    #now these are the parameters set by us based on experience
    #entry_rsi is the rsi when we enter a trade
    #we would exit the trade based on two conditions
    #one is that we hold the stock for more than five days
    #the variable for five days is called exit_days
    #we use a variable called counter to keep track of it
    #two is that rsi has increased more than 4 since the entry
    #the variable for 4 is called exit_rsi
    #when either condition is triggered, exit boolean variable gets True
    #we exit the trade
    #this is a lazy way to exit the trade
    #cuz i dont wanna import indicators from other scripts
    #i would suggest people to use other indicators such as macd or bollinger bands
    #exiting trades based on rsi is definitely inefficient and unprofitable
    entry_rsi=0.0
    counter=0
    exit_rsi=4
    exit_days=5    
    exit=False
    
    #signal generation
    for i in range(period+lag,len(df)):
        
        #this is pretty much the same idea as in bollinger bands
        #except we have two variables
        #one for shoulder and one for the bottom nodes
        moveon=False
        top=0.0
        bottom=0.0
        
        #we have to make sure no holding positions
        #and the close price is not the maximum point of pattern finding horizon
        if (df['cumsum'][i]==0) and  \
        (df['Close'][i]!=max(df['Close'][i-period:i])):
            
            j=df.index.get_loc(df['Close'][i-period:i].idxmax())
            if (np.abs(df['Close'][j]-df['Close'][i])>head*delta):
                bottom=df['Close'][i]
                moveon=True
            
            if moveon==True:
                moveon=False
                for k in range(j,i):    
                    if (np.abs(df['Close'][k]-bottom)<delta):
                        moveon=True
                        break
                        
            if moveon==True:
                moveon=False
                for l in range(j,i-period+1,-1):
                    if (np.abs(df['Close'][l]-bottom)<delta):
                        moveon=True
                        break
                    
            if moveon==True:
                moveon=False        
                for m in range(i-period,l):
                    if (np.abs(df['Close'][m]-bottom)<delta):
                        moveon=True
                        break
            
            if moveon==True:
                moveon=False        
                n=df.index.get_loc(df['Close'][m:l].idxmax())
                if (df['Close'][n]-bottom>shoulder*delta) and \
                (df['Close'][j]-df['Close'][n]>shoulder*delta):
                    top=df['Close'][n]
                    moveon=True
                    
                    
            if moveon==True:        
                for o in range(k,i):
                    if (np.abs(df['Close'][o]-top)<delta):
                        df.at[df.index[i],'signals']=-1
                        df.at[df.index[i],'coordinates']='%s,%s,%s,%s,%s,%s,%s'%(m,n,l,j,k,o,i)
                        df['cumsum']=df['signals'].cumsum()
                        entry_rsi=df['rsi'][i]
                        moveon=True
                        break
                    
        if entry_rsi!=0:
            counter+=1
            if (df['rsi'][i]-entry_rsi>exit_rsi) or \
            (counter>exit_days):
                exit=True
            
        if (df['cumsum'][i]!=0) and \
        (exit==True) and \
        (moveon==False):
            df.at[df.index[i],'signals']=1
            df['cumsum']=df['signals'].cumsum()
            exit=False
            counter=0
            entry_rsi=0
            
    return df


def pattern_plot(new,ticker):
    
    a,b=list(new[new['signals']!=0].iloc[2:4].index)
    
    temp=list(map(int,new['coordinates'][a].split(',')))
    indexlist=list(map(lambda x:new.index[x],temp))
    
    c=new.index.get_loc(b)
    newbie=new[temp[0]-30:c+20]
    
    ax=plt.figure(figsize=(10,10)).add_subplot(211)
        
    newbie['Close'].plot(label=ticker)
    ax.plot(newbie['Close'][newbie['signals']==1],marker='^',markersize=12, \
            lw=0,c='g',label='LONG')
    ax.plot(newbie['Close'][newbie['signals']==-1],marker='v',markersize=12, \
            lw=0,c='r',label='SHORT')
    
    plt.legend(loc=0)
    plt.title('Positions')
    plt.xlabel('Date')
    plt.ylabel('price')
    plt.grid(True)
    plt.show()
    
    bx=plt.figure(figsize=(10,10)).add_subplot(212,sharex=ax)
    
    newbie['rsi'].plot(label='relative strength index',c='#f4ed71')
    
    bx.fill_between(newbie.index,30,70,alpha=0.6,label='overbought/oversold range',color='#000d29')
    bx.plot(newbie['rsi'][indexlist], \
            lw=3,alpha=0.7,marker='o', \
            markersize=6,c='#8d2f23',label='head-shoulder pattern')
    bx.plot(newbie['rsi'][newbie['signals']==1],marker='^',markersize=12, \
            lw=0,c='g',label='LONG')
    bx.plot(newbie['rsi'][newbie['signals']==-1],marker='v',markersize=12, \
            lw=0,c='r',label='SHORT')

    
    for i in [(1,'Shoulder'),(3,'Head'),(5,'Shoulder')]:
        
        plt.text(indexlist[i[0]], newbie['rsi'][indexlist[i[0]]]+2, \
             '%s'%i[1],fontsize=10,color='#e4ebf2', \
             horizontalalignment='center', \
            verticalalignment='center')
        
    plt.title('RSI')
    plt.legend(loc=1)
    plt.xlabel('Date')
    plt.ylabel('value')
    plt.grid(True)
    plt.show()
    
    
# In[7]:


def main():
    
    ticker='FCAU'
    startdate='2016-01-01'
    enddate='2018-01-01'
    df=yf.download(ticker,start=startdate,end=enddate)
    new=signal_generation(df,rsi,n=14)

    plot(new,ticker)


#how to calculate stats could be found from my other code called Heikin-Ashi
# https://github.com/tattooday/quant-trading/blob/master/heikin%20ashi%20backtest.py

if __name__ == '__main__':
    main()

