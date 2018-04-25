# coding: utf-8



# In[67]:



import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import os
os.chdir('h:/')
os.getcwd()

# In[68]:
nok=pd.read_csv('nok.csv')
usd=pd.read_csv('usd.csv')
gbp=pd.read_csv('gbp.csv')
eur=pd.read_csv('eur.csv')
brent=pd.read_csv('brent.csv')


# In[69]:
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


# In[70]:
x0=pd.concat([df['usd'],df['gbp'],df['eur'],df['brent']],axis=1)
x1=sm.add_constant(x0)
x=x1[x1.index<'2017-04-25']
y=df['nok'][df.index<'2017-04-25']


# In[71]:
model=sm.OLS(y,x).fit()
print(model.summary(),'\n')

# In[72]:
upper=np.std(model.resid)
lower=-upper


# In[73]:
signals=df[df.index>='2017-04-25']
signals['fitted']=signals['usd']*model.params[1]+signals['gbp']*model.params[2]+signals['eur']*model.params[3]+signals['brent']*model.params[4]+model.params[0]
signals['upper']=signals['fitted']+0.5*upper
signals['lower']=signals['fitted']+0.5*lower
signals['stop profit']=signals['fitted']+2*upper
signals['stop loss']=signals['fitted']+2*lower
signals['signals']=0


# In[83]:
for j in signals.index:
    if pd.Series(signals['nok'])[j]>pd.Series(signals['upper'])[j]:
        signals['signals'][j:j]=-1  
          
    if pd.Series(signals['nok'])[j]<pd.Series(signals['lower'])[j]:
        signals['signals'][j:j]=1 
       
    signals['cumsum']=signals['signals'].cumsum()

    if pd.Series(signals['cumsum'])[j]>1 or pd.Series(signals['cumsum'])[j]<-1:
        signals['signals'][j:j]=0
  
    if pd.Series(signals['nok'])[j]>pd.Series(signals['stop profit'])[j]:         
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][j:j]=-signals['cumsum'][j:j]+1
        signals['cumsum']=signals['signals'].cumsum()
        break

    if pd.Series(signals['nok'])[j]<pd.Series(signals['stop loss'])[j]:
        signals['cumsum']=signals['signals'].cumsum()
        signals['signals'][j:j]=-signals['cumsum'][j:j]-1
        signals['cumsum']=signals['signals'].cumsum()
        break

# In[84]:
fig=plt.figure()
ax=fig.add_subplot(111)
signals['nok'].plot(label='jpynok')
ax.plot(signals.loc[signals['signals']>0].index,signals['nok'][signals['signals']>0],lw=0,marker='^',c='g',label='long')
ax.plot(signals.loc[signals['signals']<0].index,signals['nok'][signals['signals']<0],lw=0,marker='v',c='r',label='short')
plt.legend()
plt.title('jpynok positions')
plt.ylabel('jpynok')
plt.show()


# In[85]:
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
plt.ylabel('brent future contract in jpy')
plt.show()


# In[96]:
capital0=5000
positions=100
portfolio=pd.DataFrame(index=signals.index)
portfolio['holding']=signals['nok']*signals['cumsum']*positions
portfolio['cash']=capital0-(signals['nok']*signals['signals']*positions).cumsum()
portfolio['total asset']=portfolio['holding']+portfolio['cash']
portfolio['signals']=signals['signals']



# In[98]:
fig=plt.figure()
ax=fig.add_subplot(111)
portfolio['total asset'].plot()
ax.plot(portfolio.loc[portfolio['signals']>0].index,portfolio['total asset'][portfolio['signals']>0],lw=0,marker='^',c='g',label='long')
ax.plot(portfolio.loc[portfolio['signals']<0].index,portfolio['total asset'][portfolio['signals']<0],lw=0,marker='v',c='r',label='short')
plt.legend()
plt.title('portfolio performance')
plt.ylabel('asset value')
plt.show()
