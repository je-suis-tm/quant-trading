# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import re

os.chdir('d:/')
df=pd.read_csv('urals crude rubaud.csv')


# In[2]:


df.set_index('date',inplace=True)
df.index=pd.to_datetime(df.index)
df.dropna(inplace=True)


# In[3]:

#this is the part to create r squared of different regressors 
#in different years for stepwise regression
#we can use locals to create lists for different currency
#each list contains r squared of different years
year=df.index.year.drop_duplicates().tolist()
var=locals()
for i in df.columns:
    if i!='rub':
        var[i]=[]
        for j in year:
            x=sm.add_constant(df[i][str(j):str(j)])
            y=df['rub'][str(j):str(j)]
            m=sm.OLS(y,x).fit()
            var[i].append(m.rsquared)
           

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#to save you from the hassle
#just use these codes to generate the bar chart
width=0.3
colorlist=['#c0334d','#d6618f','#f3d4a0','#f1931b']
bar=locals()
for j in range(len(year)):
    bar[j]=[var[i][j] for i in df.columns if i!='rub']
    plt.bar(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+j*width,            
            bar[j],width=width,label=year[j],color=colorlist[j])
    
plt.legend(loc=0)
plt.title('Stepwise Regression Year by Year')
plt.ylabel('R Squared')
plt.xlabel('Regressors')
plt.xticks(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+(len(year)-1)*width/2,            
           ['Urals Crude', 'Japanese\nYen',             
            'Euro', 'Henry Hub', 'Chinese\nYuan',             
            'Korean\nWon', 'Ukrainian\nHryvnia'],fontsize=10)
plt.show()


# In[4]:

#this is similar to In[3]
#In[3] is r squared of each regressor in each year
#In[4] is r squared of each regressor of years cumulated
var=locals()
for i in df.columns:
    if i!='rub':
        var[i]=[]
        for j in year:
            x=sm.add_constant(df[i][:str(j)])
            y=df['rub'][:str(j)]
            m=sm.OLS(y,x).fit()
            var[i].append(m.rsquared)
           

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

width=0.3
colorlist=['#04060f','#03353e','#0294a5','#a79c93']
bar=locals()
for j in range(len(year)):
    bar[j]=[var[i][j] for i in df.columns if i!='rub']
    plt.bar(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+j*width,            
            bar[j],width=width,label=year[j],color=colorlist[j])
    
plt.legend(loc=0)
plt.title('Stepwise Regression Year Cumulated')
plt.ylabel('R Squared')
plt.xlabel('Regressors')
plt.xticks(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+(len(year)-1)*width/2,            
           ['Urals Crude', 'Japanese\nYen',             
            'Euro', 'Henry Hub', 'Chinese\nYuan',             
            'Korean\nWon', 'Ukrainian\nHryvnia'],fontsize=10)
plt.show()


# In[5]:

#print model summary and actual vs fitted line chart
x=sm.add_constant(pd.concat([df['urals']],axis=1))
y=df['rub']
m=sm.OLS(y['2017':'2018'],x['2017':'2018']).fit()
print(m.summary())

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(df.loc['2017':'2018'].index,m.predict(), \
        c='#0abda0',label='Fitted')
ax.plot(df.loc['2017':'2018'].index, \
        df['rub']['2017':'2018'],c='#132226',label='Actual')
plt.legend(loc=0)
plt.title('Russian Ruble 2017-2018')
plt.ylabel('RUBAUD')
plt.xlabel('Date')
plt.show()


# In[6]:

#print model summary and actual vs fitted line chart
x=sm.add_constant(pd.concat([df['urals'],df['eur']],axis=1))
y=df['rub']
m=sm.OLS(y[:'2016'],x[:'2016']).fit()
print(m.summary())
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.plot(df.loc[:'2016'].index,m.predict(), \
         c='#c05640',label='Fitted')
plt.plot(df.loc[:'2016'].index,df['rub'][:'2016'], \
         c='#edd170',label='Actual')
plt.legend(loc=0)
plt.title('Russian Ruble Before 2017')
plt.ylabel('RUBAUD')
plt.xlabel('Date')
plt.show()


# In[7]:

#normalize different regressors by 100 as the initial value
#so that we can observe the trend of different regressors in the same scale
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['urals']['2017':'2018']/df['urals']['2017':'2018'].iloc[0]*100).plot(label='Urals Crude',c='#728ca3',alpha=0.5)
(df['jpy']['2017':'2018']/df['jpy']['2017':'2018'].iloc[0]*100).plot(label='Japanese Yen',c='#99bfaa')
(df['eur']['2017':'2018']/df['eur']['2017':'2018'].iloc[0]*100).plot(label='Euro',c='#5c868d')
(df['rub']['2017':'2018']/df['rub']['2017':'2018'].iloc[0]*100).plot(label='Russian Ruble',c='#000000')
plt.legend(loc=0)
plt.title('2017-2018 Trend')
plt.ylabel('Normalized Value by 100')
plt.xlabel('Date')
plt.show()


# In[8]:

#plot actual vs fitted line chart for each year
#including one sigma and two sigma confidence interval
for i in df.index.year.drop_duplicates():
    
    temp=df.loc[str(i):str(i)]
    train=temp.iloc[:int(len(temp)/3)]
    test=temp.iloc[int(len(temp)/3):]
    x=sm.add_constant(train['urals'])
    y=train['rub']
    m=sm.OLS(y,x).fit()
    forecast=m.predict(sm.add_constant(test['urals']))
    resid=np.std(train['rub']-m.predict())
    
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.plot(test.index, \
            forecast, \
            label='Fitted',c='#f5ca99')
    test['rub'].plot(label='Actual',c='#ed5752')
    
    
    ax.fill_between(test.index, \
                    forecast+resid, \
                    forecast-resid, \
                    color='#1e1f26', \
                    alpha=0.8, \
                    label='1 Sigma')
    
    ax.fill_between(test.index, \
                    forecast+2*resid, \
                    forecast-2*resid, \
                    color='#d0e1f9', \
                     alpha=0.7, \
                     label='2 Sigma')
    
    plt.legend(loc='best')
    plt.title(f'{i} Russian Ruble Positions\nR Squared {round(m.rsquared*100,2)}%\n')
    plt.ylabel('RUBAUD')
    plt.xlabel('Date')
    plt.legend()
    plt.show()

