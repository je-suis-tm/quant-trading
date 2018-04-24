
# coding: utf-8

# In[ ]:


# coding: utf-8

# In[1]:


import statsmodels.api as sm
import pandas as pd
import numpy as np
import os
os.chdir('h:/')
os.getcwd()


# In[3]:


nok=pd.read_csv('nok.csv')
usd=pd.read_csv('usd.csv')
gbp=pd.read_csv('gbp.csv')
eur=pd.read_csv('eur.csv')
brent=pd.read_csv('brent.csv')


# In[4]:


for i in nok,usd,gbp,eur,brent:
    i.set_index(pd.to_datetime(i['Date']),inplace=True)
temp=pd.concat([nok['Last'],usd['Open'],eur['Last'],gbp['Last']],axis=1)
temp.columns=['nok','usd','eur','gbp']
temp['Date']=temp.index
crude=pd.DataFrame()
crude['brent']=brent['Last']
crude['Date']=brent.index

df=pd.merge(temp,crude)
df.set_index(pd.to_datetime(df['Date']),inplace=True)
del df['Date']


# In[5]:


x0=pd.concat([df['usd'],df['gbp'],df['eur'],df['brent']],axis=1)
x1=sm.add_constant(x0)
x=x1[x1.index<'2017-04-25']
y=df['nok'][df.index<'2017-04-25']


# In[6]:


model=sm.OLS(y,x).fit()
print(model.summary(),'\n')


# In[7]:


upper=np.std(model.resid)
lower=-upper


# In[34]:


signals=df[df.index>='2017-04-25']
signals['fitted']=signals['usd']*model.params[1]+signals['gbp']*model.params[2]+signals['eur']*model.params[3]+signals['brent']*model.params[4]+model.params[0]

signals['upper']=signals['fitted']+0.5*upper
signals['lower']=signals['fitted']+0.5*lower
signals['stop profit']=signals['fitted']+2*upper
signals['stop loss']=signals['fitted']+2*lower


# In[51]:



# In[53]:


import matplotlib.pyplot as plt
signals['fitted'].plot()
signals['nok'].plot()
signals['upper'].plot(linestyle='--')
signals['lower'].plot(linestyle='--')
signals['stop profit'].plot(linestyle=':')
signals['stop loss'].plot(linestyle=':')
plt.legend(loc='best')
plt.title('fitted vs actual')
plt.ylabel('jpynok')
plt.show()


#saudi and iran endorsed an extension of production caps
#donald trump got elected as potus
(signals['brent'][signals['stop profit']<signals['nok']]).plot(c='#FFA07A')
plt.legend(loc='best')
plt.title('brent crude after 2017/10/28')
plt.ylabel('brent future contract in usd')
plt.show()

