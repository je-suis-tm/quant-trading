
# coding: utf-8

# In[1]:


# https://www.fidelity.com/learning-center/investment-products/options/options-strategy-guide/long-straddle

# http://base2.optionsdatamine.com/page.php
# https://www.historicaloptiondata.com/

import os
os.chdir('d:/')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


# In[2]:

def find_strike_price(df):
    
    temp=[re.search('\d{4}',i).group() for i in df.columns]
    target=[]

    for i in set(temp):
        if temp.count(i)>1:
            target.append(i)
            
    return target



# In[3]:

def straddle(options,spot,contractsize,strikeprice):
        
    option=options[[i for i in options.columns if strikeprice in i]] 
    
    df=pd.merge(spot,option,left_index=True,right_index=True)

    temp=[]
    for i in df.columns:
        if 'C'+strikeprice in i:
            temp.append('call')
        elif 'P'+strikeprice in i:
            temp.append('put')
        elif 'Index' in i:
            temp.append('spot')
        else:
            temp.append(i)

    df.columns=temp
    
    df['spot']=df['spot'].apply(lambda x:x*contractsize)
    
    return df



# In[4]:


def signal_generation(df,threshold):
    
    df['signals']=np.where(
        np.abs(
            df['call']-df['put'])<threshold,
        1,0)  

    return df


# In[5]:


def plot(df,strikeprice,contractsize):
    
    ind=df[df['signals']!=0].index

    if ind.empty:
        print('Strike Price at',strikeprice,'\nNo trades available.\n')
        return 
    
    profit=np.abs(
        df['spot'].iloc[-1]-int(strikeprice)*contractsize
    )-df['call'][ind[0]]-df['put'][ind[0]]

    y=[]
    
    begin=round(int(strikeprice)*contractsize-5*(df['call'][ind[0]]+df['put'][ind[0]]),0)
    end=round(int(strikeprice)*contractsize+5*(df['call'][ind[0]]+df['put'][ind[0]]),0)+1
    
    x=list(np.arange(int(begin),int(end)))
    group1,group2=-10,-10
    for j in x:
        temp=np.abs(j-int(strikeprice)*contractsize)-(df['call'][ind[0]]+df['put'][ind[0]])
        y.append(temp)
        if temp<0 and group1<0:
            group1=x.index(j)
        if temp>0 and group1>0 and group2<0:
            group2=x.index(j)
        

    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.plot(x[:group1],y[:group1],c='#57bc90',lw=5)
    plt.plot(x[group2:],y[group2:],c='#57bc90',lw=5)
    plt.plot(x[group1:group2],y[group1:group2],c='#ec576b',lw=5)
    plt.plot([int(strikeprice)*contractsize,
              int(strikeprice)*contractsize],
              [0,-(df['call'][ind[0]]+df['put'][ind[0]])],
              linestyle=':',lw=3,c='#ec576b',alpha=0.5)
    plt.axvline(df['spot'].iloc[-1],lw=5,
                linestyle='--',c='#e5e338',alpha=0.5)

    plt.annotate('Strike Price',
                 xy=(int(strikeprice)*contractsize,
                     0),
                 xytext=(int(strikeprice)*contractsize,
                     df['call'][ind[0]]+df['put'][ind[0]]),
                 arrowprops=dict(arrowstyle='simple',
                                 facecolor='#c5c1c0',),
                 va='center',ha='center'
                 )
 
    plt.annotate('Lower Breakeven Point',
                 xy=(int(strikeprice)*contractsize-(df['call'][ind[0]]+df['put'][ind[0]]),
                     0),
                 xytext=(int(strikeprice)*contractsize-1.5*(df['call'][ind[0]]+df['put'][ind[0]]),
                         -df['call'][ind[0]]-df['put'][ind[0]]),
                 arrowprops=dict(arrowstyle='simple',
                                 facecolor='#c5c1c0'),
                 va='center',ha='center'
                 )
 
    plt.annotate('Upper Breakeven Point',
                 xy=(int(strikeprice)*contractsize+(df['call'][ind[0]]+df['put'][ind[0]]),
                     0),
                 xytext=(int(strikeprice)*contractsize+1.5*(df['call'][ind[0]]+df['put'][ind[0]]),
                         -df['call'][ind[0]]-df['put'][ind[0]]),
                 arrowprops=dict(arrowstyle='simple',
                                 facecolor='#c5c1c0'),
                 va='center',ha='center'
                 )

    plt.annotate('Spot Price',
                 xy=(df['spot'].iloc[-1],
                     2*(df['call'][ind[0]]+df['put'][ind[0]])),
                 xytext=(df['spot'].iloc[-1]*1.003,
                         2*(df['call'][ind[0]]+df['put'][ind[0]])),
                 arrowprops=dict(arrowstyle='simple',
                                 facecolor='#c5c1c0'),
                 va='center',ha='left'
                 )

    plt.locator_params(axis='x',nbins=3)
    plt.title(f'Long Straddle Options Strategy\nP&L {round(profit,2)}')
    plt.ylabel('Profit & Loss')
    plt.xlabel('Price',labelpad=50)
    plt.show()


# In[6]:


contractsize=10
threshold=2


# In[7]:

def main():
    
    data=pd.ExcelFile('stoxx50.xlsx')
    
    aug=data.parse('aug')
    aug.set_index('Dates',inplace=True)
    aug.index=pd.to_datetime(aug.index)
    
    spot=data.parse('spot')
    spot.set_index('Dates',inplace=True)
    spot.index=pd.to_datetime(spot.index)
    
    target=find_strike_price(aug)
    
    for strikeprice in target:
      
        df=straddle(aug,spot,contractsize,strikeprice)
        
        signal=signal_generation(df,threshold)
        
        plot(signal,strikeprice,contractsize)


# In[8]:


if __name__ == '__main__':
    main()


