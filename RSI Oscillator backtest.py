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
#as i have written similar strategy for bollinger bands
#plz refer to that script for more details
# https://github.com/tattooday/quant-trading/blob/master/Bollinger%20Bands%20Pattern%20Recognition%20backtest.py


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

