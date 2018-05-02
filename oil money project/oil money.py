# coding: utf-8
# In[67]:

#i call it oil money
#cuz its a statistical arbitrage on oil price and currency pair
#the inspiration came from an article i read last week
#it suggested to trade on forex of oil producing countries
#as the oil price went uprising
#what i intend to do is to build up a model
#we do a regression on historical datasets
#we use linear regression to do the prediction
#we set up thresholds based on the standard deviation of residual
#i take one deviation above as the upper threshold
#if the currency price breaches the upper threshold
#i take a short position as it is assumed to revert to its normal price range
#for the lower threshold, vice versa
#however, our regression is based on statistics
#we still need to consider fundamental influence
#what if the market condition has changed
#in that case our model wont work any more
#the price would deviate two sigmas away from predicted value
#which we should revert our positions
#e.g. the price is two sigmas above our predicted value
#we change our short to long as the market has changed
#there is probably hidden information in the uprising price
#lets follow the trend and see how it goes

#this idea sounds very silly
#nobody actually does it
#it came to my mind outta nowhere
#i just wanna see if this project is plausible
#perhaps im gonna suffer a huge loss from it
#however, its not what i thought it was
#it turned out to be a totally different indicator!
#first, we choose my currency norwegian krone
#norway is one of the largest oil producing countries with floating fx regime
#other oil producing countries such as saudi, iran, qatar have their fx pegged to usd
#russia is supposed to be a good training set
#nevertheless, russia got sanctioned by uncle sam a lot
#i tried rubjpy and the model barely captured anything
#every model seemed to be overfitted and had no prediction power
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
os.chdir('h:/')
os.getcwd()


# In[68]:
#this part is just data etl
#i got my raw data from eikon 4 
#so i gotta consolidate em before regression
#i have uploaded integrated dataset called raw.csv in this folder
#u can use pd.read_csv to replace this section
nok=pd.read_csv('nok.csv')
usd=pd.read_csv('usd.csv')
gbp=pd.read_csv('gbp.csv')
eur=pd.read_csv('eur.csv')
brent=pd.read_csv('brent.csv')
# In[69]:
#this loop is unnecessary
#i am just being lazy
#lets turn these prices into time series
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
df.to_csv('raw.csv')



# In[70]:
#now we do our linear regression
#lets denote data from 2013-4-25 to 2017-4-25 as estimation window
#lets denote data from 2017-4-25 to 2018-4-25 as backtesting window
x0=pd.concat([df['usd'],df['gbp'],df['eur'],df['brent']],axis=1)
x1=sm.add_constant(x0)
x=x1[x1.index<'2017-04-25']
y=df['nok'][df.index<'2017-04-25']
model=sm.OLS(y,x).fit()
print(model.summary(),'\n')
#nevertheless, from the summary u can tell there is multicollinearity
#alternatively, i can use elastic net regression to achieve the convergence

m=en(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10], \
l1_ratio=[.01, .1, .5, .9, .99],  max_iter=5000).fit(x0[x0.index<'2017-04-25'], y)  
print(m.intercept_,m.coef_)

#elastic net estimation results:
#3.79776228406 [ 0.00388958  0.01992038  0.02823187  0.00050092]


#we plot the difference between two different approaches
#note that the difference is negative skewed
df['fit1']=df['usd']*m.coef_[0]+df['gbp']*m.coef_[1]+df['eur']*m.coef_[2]+df['brent']*m.coef_[3]+m.intercept_
df['fit2']=df['usd']*model.params[1]+df['gbp']*model.params[2]+df['eur']*model.params[3]+df['brent']*model.params[4]+model.params[0]
df['epsilon']=df['fit1']-df['fit2']
df['epsilon'].hist()
plt.title('ols vs elastic net')
plt.legend()
plt.show()
print(adf(df['epsilon']))

#unit root test results:
#(-2.4689818197725981, 0.12320492058022914, 2, 1286, {'1%': -3.4354451795550935, '5%': -2.863790090661305, '10%': -2.5679679660127368}, -6151.8371655225037)
#hence, its not a stationary process

#next step is to compare mean and standard deviation of two approaches
df['residual 1']=df['nok']-df['fit1']
df['residual 2']=df['nok']-df['fit2']
print(np.mean(df['residual 1'])>np.mean(df['residual 2']))
print(np.std(df['residual 1'])>np.std(df['residual 2']))

#boolean values:
#True
#False
#thus, ols overestimates the price 
#elastic net has a smaller standard deviation
#ols may be biased subject to multicollinearity
#apparently we got a winner

# In[72]:
#lets generate signals based on the winner
#we set one sigma of the residual as thresholds
#two sigmas of the residual as stop orders
#which is common practise in statistics
upper=np.std(df['residual 2'][df.index<'2017-04-25'])
lower=-upper
signals=df[df.index>='2017-04-25']
signals['fitted']=df['fit1']
signals['upper']=signals['fitted']+0.5*upper
signals['lower']=signals['fitted']+0.5*lower
signals['stop profit']=signals['fitted']+2*upper
signals['stop loss']=signals['fitted']+2*lower
signals['signals']=0



# In[83]:
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
#next, we plot the usual positions as the first figure
fig=plt.figure()
ax=fig.add_subplot(111)
signals['nok'].plot(label='nokjpy')
ax.plot(signals.loc[signals['signals']>0].index,signals['nok'][signals['signals']>0],lw=0,marker='^',c='g',label='long')
ax.plot(signals.loc[signals['signals']<0].index,signals['nok'][signals['signals']<0],lw=0,marker='v',c='r',label='short')
plt.axvline('2017/11/15',linestyle=':',c='k',label='stop order')
plt.legend()
plt.title('nokjpy positions')
plt.ylabel('nokjpy')
plt.show()


# In[85]:
#the second figure explores thresholds and boundaries for signal generation
#we can see after 2017/11/15, nokjpy price went skyrocketing
#as a data scientist, we must ask why?
#is it a problem of our model identification
#or the fundamental situation of nokjpy or oil price changed
signals['fitted'].plot(alpha=0.2)
signals['nok'].plot()
signals['upper'].plot(linestyle=':')
signals['lower'].plot(linestyle=':')
signals['stop profit'].plot(linestyle='--')
signals['stop loss'].plot(linestyle='--')
plt.legend(loc='best')
plt.title('fitted vs actual')
plt.ylabel('nokjpy')
plt.show()

#if we decompose nokjpy into long term trend and short term random process
#we could clearly see that brent crude price has dominated short term random process
#so what changed the long term trend?
#there are a few possible reasons
#saudi and iran endorsed an extension of production caps on that particular date
#donald trump got elected as potus so he would encourage a depreciated us dollar
#which ultimately pushed up the oil price
(signals['brent'][signals['stop loss']>signals['nok']]).plot(c='#FFA07A')
plt.legend(loc='best')
plt.title('brent crude after 2017/11/15')
plt.ylabel('brent future contract in jpy')
plt.show()

#lets normalize all prices by 100
#its easy to see that nok follows euro
#and economics explanation would be norway is in eea
#its economy heavily relies on eu
(df['nok']/df['nok'][0]*100).plot()
(df['usd']/df['usd'][0]*100).plot()
(df['eur']/df['eur'][0]*100).plot()
(df['gbp']/df['gbp'][0]*100).plot()
(df['brent']/df['brent'][0]*100).plot()
plt.legend()
plt.ylabel('normalized price by 100')
plt.title('random walk with a drift')
plt.show()

# In[96]:
#then lets do a pnl analysis
capital0=2000
positions=100
portfolio=pd.DataFrame(index=signals.index)
portfolio['holding']=signals['nok']*signals['cumsum']*positions
portfolio['cash']=capital0-(signals['nok']*signals['signals']*positions).cumsum()
portfolio['total asset']=portfolio['holding']+portfolio['cash']
portfolio['signals']=signals['signals']

# In[98]:
#we plot how our asset value changes over time
fig=plt.figure()
ax=fig.add_subplot(111)
portfolio['total asset'].plot()
ax.plot(portfolio.loc[portfolio['signals']>0].index,portfolio['total asset'][portfolio['signals']>0],lw=0,marker='^',c='g',label='long')
ax.plot(portfolio.loc[portfolio['signals']<0].index,portfolio['total asset'][portfolio['signals']<0],lw=0,marker='v',c='r',label='short')
plt.axvline('2017/11/15',linestyle=':',c='k',label='stop order')
plt.legend()
plt.title('portfolio performance')
plt.ylabel('asset value')
plt.show()

#surprising when our model is valid for prediction
#its difficult to make money from thresholds oscillating
#when actual price goes beyond stop order boundary
#that is basically the most profitable trade ever
#best to follow up with a momentum strategy
#maybe this is not a statistical arbitrage after all
#the model is a trend following indicator
#i just created a momentum trading strategy
