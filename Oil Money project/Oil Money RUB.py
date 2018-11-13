
# coding: utf-8

# In[1]:


# https://en.wikipedia.org/wiki/List_of_countries_by_exchange_rate_regime
# http://www.worldstopexports.com/omans-top-10-exports/
# https://www.rferl.org/a/russia-sanctions-timeline/29477179.html
import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import re


# In[2]:


os.chdir('d:/')


# In[3]:


df=pd.read_csv('urals crude rubaud.csv')


# In[4]:


df.set_index('date',inplace=True)
df.index=pd.to_datetime(df.index)


# In[5]:


df.dropna(inplace=True)


# In[6]:


year=df.index.year.drop_duplicates().tolist()


# In[7]:


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

width=0.3
colorlist=['#c0334d','#d6618f','#f3d4a0','#f1931b']
bar=locals()
for j in range(len(year)):
    bar[j]=[var[i][j] for i in df.columns if i!='rub']
    plt.bar(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+j*width,            bar[j],width=width,label=year[j],color=colorlist[j])
    
plt.legend(loc=0)
plt.title('Stepwise Regression Year by Year')
plt.ylabel('R Squared')
plt.xlabel('Regressors')
plt.xticks(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+(len(year)-1)*width/2,            ['Urals Crude', 'Japanese\nYen',             'Euro', 'Henry Hub', 'Chinese\nYuan',             'Korean\nWon', 'Ukrainian\nHryvnia'],fontsize=10)
plt.show()


# In[8]:


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
    plt.bar(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+j*width,            bar[j],width=width,label=year[j],color=colorlist[j])
    
plt.legend(loc=0)
plt.title('Stepwise Regression Year Cumulated')
plt.ylabel('R Squared')
plt.xlabel('Regressors')
plt.xticks(np.arange(1,len([i for i in df.columns if i!='rub'])*2+1,2)+(len(year)-1)*width/2,            ['Urals Crude', 'Japanese\nYen',             'Euro', 'Henry Hub', 'Chinese\nYuan',             'Korean\nWon', 'Ukrainian\nHryvnia'],fontsize=10)
plt.show()


# In[9]:


x=sm.add_constant(pd.concat([df['urals']],axis=1))
y=df['rub']
m=sm.OLS(y['2018':'2018'],x['2018':'2018']).fit()
print(m.summary())

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(df.loc['2018':'2018'].index,m.predict(),c='#0abda0',label='Fitted')
ax.plot(df.loc['2018':'2018'].index,df['rub']['2018':'2018'],c='#132226',label='Actual')
plt.legend(loc=0)
plt.title('Russian Ruble 2018')
plt.ylabel('RUBAUD')
plt.xlabel('Date')
plt.show()


# In[10]:


x=sm.add_constant(pd.concat([df['urals'],df['eur']],axis=1))
y=df['rub']
m=sm.OLS(y[:'2017'],x[:'2017']).fit()
print(m.summary())
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.plot(df.loc[:'2017'].index,m.predict(),c='#c05640',label='Fitted')
plt.plot(df.loc[:'2017'].index,df['rub'][:'2017'],c='#edd170',label='Actual')
plt.legend(loc=0)
plt.title('Russian Ruble Before 2018')
plt.ylabel('RUBAUD')
plt.xlabel('Date')
plt.show()


# In[11]:


ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['urals']['2018']/df['urals']['2018'].iloc[0]*100).plot(label='Urals Crude',c='#728ca3')
(df['jpy']['2018']/df['jpy']['2018'].iloc[0]*100).plot(label='Japanese Yen',c='#99bfaa')
(df['eur']['2018']/df['eur']['2018'].iloc[0]*100).plot(label='Euro',c='#5c868d')
(df['rub']['2018']/df['rub']['2018'].iloc[0]*100).plot(label='Russian Ruble',c='#000000')
plt.legend(loc=0)
plt.title('2018 Trend')
plt.ylabel('Normalized Value by 100')
plt.xlabel('Date')
plt.show()

