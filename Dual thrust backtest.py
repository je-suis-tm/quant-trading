# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 15:22:38 2018

@author: Administrator
"""

import os
os.chdir('D:/')
os.getcwd()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#
df=pd.read_csv('eurusd.csv')
df.set_index(pd.to_datetime(df['date']),inplace=True)

rg=5
param=0.5


#
memo={'date':[],'open':[],'close':[],'high':[],'low':[]}
for i in range(1,32):
    try:
        temp=df['2018-01-%d 3:00:00'%(i):'2018-01-%d 12:00:00'%(i)]['eurusd']
        
        memo['open'].append(temp[0])
        memo['close'].append(temp[-1])
        memo['high'].append(max(temp))
        memo['low'].append(min(temp))
        memo['date'].append('2018-01-%d'%(i))
        
    except Exception:
        continue

intraday=pd.DataFrame()

for key in memo:
    intraday[key]=memo[key]

intraday.set_index(pd.to_datetime(intraday['date']),inplace=True)
intraday['range1']=intraday['high'].rolling(rg).max()-intraday['close'].rolling(rg).min()
intraday['range2']=intraday['close'].rolling(rg).max()-intraday['low'].rolling(rg).min()
intraday['range']=np.where(intraday['range1']>intraday['range2'],intraday['range1'],intraday['range2'])
    

#
signals=pd.DataFrame(df[df.index>='2018-01-08'])
signals['signals']=0
signals['cumsum']=0
sigup=float(0)
siglo=float(0)


#
for i in signals.index:
    if (i.hour==3 and i.minute==0):
        sigup=float(param*intraday['range']['2018-01-%d'%(i.day):'2018-01-%d'%(i.day)]+pd.Series(signals['eurusd'])[i])
        siglo=float(-(1-param)*intraday['range']['2018-01-%d'%(i.day):'2018-01-%d'%(i.day)]+pd.Series(signals['eurusd'])[i])

    if (sigup!=0 and pd.Series(signals['eurusd'])[i]>sigup):
        signals['signals'][i:i]=1
    if (siglo!=0 and pd.Series(signals['eurusd'])[i]<siglo):
        signals['signals'][i:i]=-1

    if pd.Series(signals['signals'])[i]!=0:
        signals['cumsum']=signals['signals'].cumsum()
        
        if (pd.Series(signals['cumsum'])[i]>1 or pd.Series(signals['cumsum'])[i]<-1):
            signals['signals'][i:i]=0
               
        if (pd.Series(signals['cumsum'])[i]==0):
            if (pd.Series(signals['eurusd'])[i]>sigup):
                signals['signals'][i:i]=2
            if (pd.Series(signals['eurusd'])[i]<siglo):
                signals['signals'][i:i]=-2
  
    if i.hour==12 and i.minute==0:
        sigup,siglo=float(0),float(0)
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][i:i]=-signals['cumsum'][i:i]
        

#
plt.style.use('ggplot')
plt.show()
signew=signals[signals.index>'2018-01-20']
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(signew['eurusd'],label='EURUSD')
ax.plot(signew.loc[signew['signals']==1].index,signew['eurusd'][signew['signals']==1],lw=0,marker='^',markersize=10,c='g',label='long')
ax.plot(signew.loc[signew['signals']==-1].index,signew['eurusd'][signew['signals']==-1],lw=0,marker='v',markersize=10,c='r',label='short')
lgd=plt.legend(loc='best').get_texts()
for text in lgd:
    text.set_color('k')
plt.ylabel('EURUSD')
plt.xlabel('date')
plt.title('positions')
plt.show()
