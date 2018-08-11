
# coding: utf-8

# In[1]:


#i call it oil money
#cuz its a statistical arbitrage on oil price and currency pair
#the inspiration came from an article i read last week
#it suggested to trade on forex of oil producing countries
#when the oil price went uprising and overall volatility for forex market was low
#what i intend to do is to build up a model to explore the causality
#we do a regression on historical datasets
#we use linear regression to make a prediction
#we set up thresholds based on the standard deviation of residual
#i take one deviation above as the upper threshold
#if the currency price breaches the upper threshold
#i take a short position as it is assumed to revert to its normal price range
#for the lower threshold, vice versa
#so its kinda like bollinger bands

#however, our regression is based on statistics
#we still need to consider fundamental influence
#what if the market condition has changed
#in that case our model wont work any more
#the price would deviate two sigmas away from predicted value
#which we should revert our positions
#e.g. the price is two sigmas above our predicted value
#we change our short to long as the market has changed its sentiment
#there is probably hidden information in the uprising price
#lets follow the trend and see where it ends

#this idea sounds very silly
#nobody actually does it or not that i knew
#it came to my mind outta nowhere
#i just wanna see if this project is plausible
#perhaps im gonna suffer a huge loss from it
#however, its not what i thought it was
#it turned out to be a totally different indicator in the end!

#first, we choose our currency norwegian krone
#norway is one of the largest oil producing countries with floating fx regime
#other oil producing countries such as saudi, iran, venezuela have their fx pegged to usd
#russia is supposed to be a good training set
#nevertheless, russia got sanctioned by uncle sam a lot
#i tried rubjpy and the model barely captured anything
#every model seemed to be overfitted and had no prediction power on rubjpy
#i have uploaded russian ruble raw data in this folder for those who are willing to try

#after targetting at norwegian krone, we have to choose a currency to evaluate nok
#i took a look at norway's biggest trading partners 
#i decided to include us dollar, euro and uk sterling as well as brent crude price in our model
#in addition, i chose japanese yen as target currency
#cuz its not a big trading partner with norway
#which implies it doesnt have much correlation with nok
#preparation is done, lets get started!

import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNetCV as en 
from statsmodels.tsa.stattools import adfuller as adf
import os
os.chdir('d:/')


# In[2]:


df=pd.read_csv('brent crude nokjpy.csv')
df.set_index(pd.to_datetime(df[list(df.columns)[0]]),inplace=True)
del df[list(df.columns)[0]]


# In[3]:


#now we do our linear regression
#lets denote data from 2013-4-25 to 2017-4-25 as estimation window/training set
#lets denote data from 2017-4-25 to 2018-4-25 as backtesting window/testing set
x0=pd.concat([df['usd'],df['gbp'],df['eur'],df['brent']],axis=1)
x1=sm.add_constant(x0)
x=x1[x1.index<'2017-04-25']
y=df['nok'][df.index<'2017-04-25']

model=sm.OLS(y,x).fit()
print(model.summary(),'\n')


# In[4]:


#nevertheless, from the summary u can tell there is multicollinearity
#the condition number is skyrocketing
#alternatively, i can use elastic net regression to achieve the convergence
m=en(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10],
     l1_ratio=[.01, .1, .5, .9, .99],  max_iter=5000).fit(x0[x0.index<'2017-04-25'], y)  
print(m.intercept_,m.coef_)


#elastic net estimation results:
#3.79776228406 [ 0.00388958  0.01992038  0.02823187  0.00050092]


# In[5]:


#we plot the difference between two different approaches
#note that the difference is negative skewed
df['sk_fit']=(df['usd']*m.coef_[0]+df['gbp']*m.coef_[1]+
                 df['eur']*m.coef_[2]+df['brent']*m.coef_[3]+m.intercept_)
df['ols_fit']=(df['usd']*model.params[1]+df['gbp']*model.params[2]+
                 df['eur']*model.params[3]+df['brent']*model.params[4]+model.params[0])
df['epsilon']=df['sk_fit']-df['ols_fit']

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

df['epsilon'].hist(histtype='bar',color='#ede574',width=0.007,bins=80)

plt.title('OLS vs Elastic Net',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(False)
plt.ylabel('Frequency')
plt.xlabel('Interval')
plt.show()

print(adf(df['epsilon']))

#unit root test results:
#(-2.4689818197725981, 0.12320492058022914, 2, 1286, {'1%': -3.4354451795550935, '5%': -2.863790090661305, '10%': -2.5679679660127368}, -6151.8371655225037)
#hence, its not a stationary process


# In[6]:


#next step is to compare mean and standard deviation of two approaches
df['sk_residual']=df['nok']-df['sk_fit']
df['ols_residual']=df['nok']-df['ols_fit']

print(np.mean(df['sk_residual'])>np.mean(df['ols_residual']))
print(np.std(df['sk_residual'])>np.std(df['ols_residual']))

#boolean values:
#True
#False
#assuming elastic net correctly estimate the price
#thus, ols overestimates the price a lot
#elastic net has a smaller standard deviation after recalibration
#ols may be biased subject to multicollinearity
#apparently we got a winner


# In[7]:


#lets generate signals based on the winner
#we set one sigma of the residual as thresholds
#two sigmas of the residual as stop orders
#which is common practise in statistics
upper=np.std(df['sk_residual'][df.index<'2017-04-25'])
lower=-upper

signals=pd.concat([df[i] for i in ['nok', 'usd', 'eur', 'gbp', 'brent', 'sk_fit','sk_residual']],                   axis=1)[df.index>='2017-04-25']
signals['fitted']=signals['sk_fit']
del signals['sk_fit']

signals['upper']=signals['fitted']+upper
signals['lower']=signals['fitted']+lower
signals['stop profit']=signals['fitted']+2*upper
signals['stop loss']=signals['fitted']+2*lower
signals['signals']=0


# In[8]:


#while doing a traversal
#we apply the rules mentioned before
#if actual price goes beyond upper threshold
#we take a short and bet on its reversion process
#vice versa
#we use cumsum to make sure our signals only get generated
#for the first time condions are met
#when actual price hits the stop order boundary
#we revert our positions
#u may wonder whats next for breaking the boundary
#well, we stop the signal generation algorithm
#we need to recalibrate our model or use other trend following strategies
#i will leave this part to u
index=list(signals.columns).index('signals')

for j in range(len(signals)):
    
    if signals['nok'].iloc[j]>signals['upper'].iloc[j]:
        signals.iloc[j,index]=-1  
          
    if signals['nok'].iloc[j]<signals['lower'].iloc[j]:
        signals.iloc[j,index]=1 
       
    signals['cumsum']=signals['signals'].cumsum()

    if signals['cumsum'].iloc[j]>1 or signals['cumsum'].iloc[j]<-1:
        signals.iloc[j,index]=0
  
    if signals['nok'].iloc[j]>signals['stop profit'].iloc[j]:         
        signals['cumsum']=signals['signals'].cumsum()
        signals.iloc[j,index]=-signals['cumsum'].iloc[j]+1
        signals['cumsum']=signals['signals'].cumsum()
        break

    if signals['nok'].iloc[j]<signals['stop loss'].iloc[j]:
        signals['cumsum']=signals['signals'].cumsum()
        signals.iloc[j,index]=-signals['cumsum'].iloc[j]-1
        signals['cumsum']=signals['signals'].cumsum()
        break


# In[9]:


#next, we plot the usual positions as the first figure
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

signals['nok'].plot(label='NOKJPY',c='#594f4f',alpha=0.5)
ax.plot(signals.loc[signals['signals']>0].index,
         signals['nok'][signals['signals']>0],
         lw=0,marker='^',c='#83af9b',label='LONG', markersize=10)
ax.plot(signals.loc[signals['signals']<0].index,
         signals['nok'][signals['signals']<0],
         lw=0,marker='v',c='#fe4365',label='SHORT', markersize=10)
ax.plot(pd.to_datetime('2017-12-20'),
         signals['nok'].loc['2017-12-20'],
         lw=0,marker='*',c='#f9d423', markersize=15, alpha=0.8,
         label='Potential Exit Point of Momentum Trading')

plt.axvline('2017/11/15',linestyle=':',c='k',label='Exit')
plt.legend()
plt.title('NOKJPY Positions')
plt.ylabel('NOKJPY')
plt.xlabel('Date')
plt.show()


# In[10]:


#the second figure explores thresholds and boundaries for signal generation
#we can see after 2017/11/15, nokjpy price went skyrocketing
#as a data scientist, we must ask why?
#is it a problem of our model identification
#or the fundamental situation of nokjpy or oil changed

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

signals['fitted'].plot(lw=2.5,label='Fitted',c='w',alpha=0.6)
signals['nok'].plot(lw=2,label='Actual',c='#04060f',alpha=0.8)
ax.fill_between(signals.index,signals['upper'],
                signals['lower'],alpha=0.2,label='1 Sigma',color='#2a3457')
ax.fill_between(signals.index,signals['stop profit'],
                signals['stop loss'],alpha=0.1,label='2 Sigma',color='#720017')

plt.legend(loc='best')
plt.title('Fitted vs Actual')
plt.ylabel('NOKJPY')
plt.xlabel('Date')
plt.show()


# In[11]:


#if we decompose nokjpy into long term trend and short term random process
#we could clearly see that brent crude price has dominated short term random process
#so what changed the long term trend?
#there are a few possible reasons
#saudi and iran endorsed an extension of production caps on that particular date
#donald trump got elected as potus so he would encourage a depreciated us dollar
#which ultimately pushed up the oil price
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(signals['brent'][signals.index>'2017-11-15']).plot(c='#355c7d',                                                    label='Brent Crude 1st Month Future Contract in JPY')

plt.legend(loc='best')
plt.title('After 2017/11/15')
plt.ylabel('JPY')
plt.xlabel('Date')
plt.show()


# In[12]:


#lets normalize all prices by 100
#its easy to see that nok follows euro
#and economics explanation would be norway is in eea
#its economy heavily relies on eu
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['nok']/df['nok'][0]*100).plot(c='#ff8c94',label='Norwegian Krone',alpha=0.9)
(df['usd']/df['usd'][0]*100).plot(c='#9de0ad',label='US Dollar',alpha=0.9)
(df['eur']/df['eur'][0]*100).plot(c='#45ada8',label='Euro',alpha=0.9)
(df['gbp']/df['gbp'][0]*100).plot(c='#f8b195',label='UK Sterling',alpha=0.9)
(df['brent']/df['brent'][0]*100).plot(c='#6c5b7c',label='Brent Crude',alpha=0.5)

plt.legend(loc='best')
plt.ylabel('Normalized Price by 100')
plt.xlabel('Date')
plt.title('Trend')
plt.show()


# In[13]:


#that still doesnt sound convincable
#lets try cointegration test
#academically we should use johansen test which works on multi dimensions
#unfortunately, there is no johansen test in statsmodels
#well, here we go again
#we have to use Engle-Granger two step!
#salute to Engle, mentor of my mentor Gallo
#to the nobel prize winner

#im not gonna explain much here
#if u have checked my other codes, u would know
#details are in pair trading session
# https://github.com/tattooday/quant-trading/blob/master/Pair%20trading%20backtest.py

x2=df['eur'][df.index<'2017-04-25']
x3=sm.add_constant(x2)

model=sm.OLS(y,x3).fit()
ero=model.resid

print(adf(ero))
print(model.summary())

#(-2.5593457642922992, 0.10169409761939013, 0, 1030, 
#{'1%': -3.4367147300588341, '5%': -2.8643501440982058, '10%': -2.5682662399849185}, -1904.8360920752475)
#0.731199409071
#unfortunately, the residual hasnt even reached 90% confidence interval
#we cant conclude any cointegration from the test
#still, from the visualization
#we can tell nok and eur are somewhat correlated
#our rsquared suggested euro has the power of 73% explanation on nok


# In[14]:


#then lets do a pnl analysis
capital0=2000
positions=100
portfolio=pd.DataFrame(index=signals.index)
portfolio['holding']=signals['nok']*signals['cumsum']*positions
portfolio['cash']=capital0-(signals['nok']*signals['signals']*positions).cumsum()
portfolio['total asset']=portfolio['holding']+portfolio['cash']
portfolio['signals']=signals['signals']


# In[15]:


portfolio=portfolio[portfolio.index>'2017-10-01']
portfolio=portfolio[portfolio.index<'2018-01-01']


# In[16]:


#we plot how our asset value changes over time
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

portfolio['total asset'].plot(c='#594f4f',alpha=0.5,label='Total Asset')
ax.plot(portfolio.loc[portfolio['signals']>0].index,portfolio['total asset'][portfolio['signals']>0],
         lw=0,marker='^',c='#2a3457',label='LONG',markersize=10,alpha=0.5)
ax.plot(portfolio.loc[portfolio['signals']<0].index,portfolio['total asset'][portfolio['signals']<0],
         lw=0,marker='v',c='#720017',label='The Big Short',markersize=15,alpha=0.5)
ax.fill_between(portfolio['2017-11-20':'2017-12-20'].index,
                 (portfolio['total asset']+np.std(portfolio['total asset']))['2017-11-20':'2017-12-20'],
                 (portfolio['total asset']-np.std(portfolio['total asset']))['2017-11-20':'2017-12-20'],
                 alpha=0.2, color='#547980')

plt.text(pd.to_datetime('2017-12-20'),
          (portfolio['total asset']+np.std(portfolio['total asset'])).loc['2017-12-20'],
          'What if we use MACD here?')
plt.axvline('2017/11/15',linestyle=':',label='Exit',c='#ff847c')
plt.legend()
plt.title('Portfolio Performance')
plt.ylabel('Asset Value')
plt.xlabel('Date')
plt.show()


#surprising when our model is valid for prediction
#its difficult to make money from thresholds oscillating
#when actual price goes beyond stop order boundary
#that is basically the most profitable trade ever
#best to follow up with a momentum strategy
#maybe this is not a statistical arbitrage after all
#the model is a trend following entry indicator
#can we do pair trading between brent crude and norwegian krone?
#absolutely not!
#but we may closely monitor the cointegration period
#prepare for a momentum following once the cointegration breaks

