
# coding: utf-8

# In[1]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
os.chdir('d:/')
import numpy as np


# In[2]:


df=pd.read_csv('wcs crude cadaud.csv',encoding='utf-8')


# In[3]:


df.set_index('date',inplace=True)


# In[4]:


df.index=pd.to_datetime(df.index,format='%m/%d/%Y')


# In[5]:


df=df.reindex(columns=
['cny',
 'gbp',
 'usd',
 'eur',
 'krw',
 'mxn',
 'gas',
 'wcs',
 'edmonton',
 'wti',
 'gold',
 'jpy',
 'cad'])


# In[6]:


var=locals()

for i in df.columns:
    if i!='cad':
            x=sm.add_constant(df[i])
            y=df['cad']
            m=sm.OLS(y,x).fit()
            var[str(i)]=m.rsquared
     
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

width=0.7
colorlist=['#9499a6','#9499a6','#9499a6','#9499a6',
           '#9499a6','#9499a6','#9499a6','#582a20',
           '#be7052','#f2c083','#9499a6','#9499a6']

temp=list(df.columns)
for i in temp:
    if i!='cad':
        plt.bar(temp.index(i)+width,            
            var[str(i)],width=width,label=i,
               color=colorlist[temp.index(i)])
 
plt.title('Regressions on Loonie')
plt.ylabel('R Squared\n')
plt.xlabel('\nRegressors')
plt.xticks(np.arange(len(temp))+width,
           ['Yuan', 'Sterling', 'Dollar', 'Euro', 'KRW',
             'MXN', 'Gas', 'WCS', 'Edmonton',
             'WTI', 'Gold', 'Yen'],fontsize=10)
plt.show()


# In[7]:


ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['cny']/df['cny'].iloc[0]).plot(c='#283670',label='Yuan')
(df['gbp']/df['gbp'].iloc[0]).plot(c='#fe4d32',label='Sterling')
(df['cad']/df['cad'].iloc[0]).plot(c='#484a25',label='Loonie')
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Loonie vs Yuan vs Sterling')
plt.show()


# In[8]:


ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['wti']/df['wti'].iloc[0]).plot(c='#2a78b2',label='WTI',alpha=0.5)
(df['wcs']/df['wcs'].iloc[0]).plot(c='#7b68ee',label='WCS',alpha=0.5)
(df['edmonton']/df['edmonton'].iloc[0]).plot(c='#110b3c',
                                             label='Edmonton',alpha=0.5)
(df['cad']/df['cad'].iloc[0]).plot(c='#cb8b8b',label='Loonie')
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Loonie vs Crude Oil Blends')
plt.show()

