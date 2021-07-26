
# coding: utf-8

# In[1]:


#i call it oil money
#cuz its a statistical arbitrage on crude benchmark and petrocurrency
#the inspiration came from an article i read
#it suggested to trade on petrocurrency when the oil price went uprising 
#plus overall volatility for forex market was low
#the first thing is to build up a model to explore the causality
#we split the historical datasets into two parts
#one for the model estimation, the other for the model validation
#we do a regression on estimation horizon
#we use linear regression to make a prediction on ideal price level
#we set up thresholds based on the standard deviation of residual
#take one deviation above as the upper threshold
#if the currency price breaches the upper threshold
#take a short position as it is assumed to revert to its 'normal' price range soon
#vice versa
#so its kinda like bollinger bands

#however, our regression is based on statistics
#we still need to consider fundamental influence
#what if the market condition has changed
#in that case our model wont work any more
#well,all models lose their creditability over the time
#denote the price deviating two sigmas away from predicted value as model failure
#which we should revert our positions
#e.g. the price is two sigmas above our predicted value
#we change our short to long since the market has changed its sentiment
#there is probably hidden information in the uprising price
#lets follow the trend and see where it ends

#this idea sounds very silly
#nobody actually does it or not that i know of
#i just wanna to see if the idea would work
#perhaps the idea would bring a huge loss
#nonetheless, it turns out to be a big surprise!

#first, we choose our currency norwegian krone
#norway is one of the largest oil producing countries with floating fx regime
#other oil producing countries such as saudi, iran, venezuela have their fx pegged to usd
#russia is supposed to be a good training set
#nevertheless, russia gets sanctioned by uncle sam a lot
#we would see this in the next script
# https://github.com/je-suis-tm/quant-trading/blob/master/Oil%20Money%20project/Oil%20Money%20RUB.py

#after targetting at norwegian krone, we have to choose a currency to evaluate nok
#take a look at norway's biggest trading partners 
#we should include us dollar, euro and uk sterling as well as brent crude price in our model
#in addition, the base currency would be japanese yen 
#cuz its not a big trading partner with norway
#which implies it doesnt have much correlation with nok
#preparation is done, lets get started!

import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import ElasticNetCV as en 
from statsmodels.tsa.stattools import adfuller as adf
import os
os.chdir('d:/')


# In[2]:


df=pd.read_csv('brent crude nokjpy.csv')
df.set_index(pd.to_datetime(df[list(df.columns)[0]]),inplace=True)
del df[list(df.columns)[0]]


# In[3]:

#identification
#first of first, using scatter plot to visualize the correlation
#lets denote data from 2013-4-25 to 2017-4-25 as estimation horizon/training set
#lets denote data from 2017-4-25 to 2018-4-25 as validation horizon/testing set
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.scatter(df['brent'][df.index<'2017-04-25'],df['nok'][df.index<'2017-04-25'],s=1,c='#5f0f4e')

plt.title('NOK Brent Correlation')
plt.xlabel('Brent in JPY')
plt.ylabel('NOKJPY')
plt.show()

#if we run a covariance matrix on nok and brent, we got
#np.corrcoef(df['nok'],df['brent'])
#array([[1.        , 0.89681228],[0.89681228, 1.        ]])


#dual axis plot
def dual_axis_plot(xaxis,data1,data2,fst_color='r',
                    sec_color='b',fig_size=(10,5),
                   x_label='',y_label1='',y_label2='',
                   legend1='',legend2='',grid=False,title=''):
    
    fig=plt.figure(figsize=fig_size)
    ax=fig.add_subplot(111)
    

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label1, color=fst_color)
    ax.plot(xaxis, data1, color=fst_color,label=legend1)
    ax.tick_params(axis='y',labelcolor=fst_color)
    ax.yaxis.labelpad=15

    plt.legend(loc=3)
    ax2 = ax.twinx()

    ax2.set_ylabel(y_label2, color=sec_color,rotation=270)
    ax2.plot(xaxis, data2, color=sec_color,label=legend2)
    ax2.tick_params(axis='y',labelcolor=sec_color)
    ax2.yaxis.labelpad=15

    fig.tight_layout()
    plt.legend(loc=4)
    plt.grid(grid)
    plt.title(title)
    plt.show()
    
#nok vs ir
dual_axis_plot(df.index,df['nok'],df['interest rate'],
               fst_color='#34262b',sec_color='#cb2800',
               fig_size=(10,5),x_label='Date',
               y_label1='NOKJPY',y_label2='Norges Bank Interest Rate 
               %',
               legend1='NOKJPY',legend2='Interest Rate',
               grid=False,title='NOK vs Interest Rate')

#nok vs brent
dual_axis_plot(df.index,df['nok'],df['brent'],
               fst_color='#4f2d20',sec_color='#3feee6',
               fig_size=(10,5),x_label='Date',
               y_label1='NOKJPY',y_label2='Brent in JPY',
               legend1='NOKJPY',legend2='Brent',
               grid=False,title='NOK vs Brent')
               
#nok vs gdp
#cuz gdp is released quarterly
#we need to convert nok into quarterly data as well
ind=df['gdp yoy'].dropna().index
dual_axis_plot(df.loc[ind].index,
               df['nok'].loc[ind],
               df['gdp yoy'].dropna(),
               fst_color='#116466',sec_color='#ff652f',
               fig_size=(10,5),x_label='Date',
               y_label1='NOKJPY',y_label2='Norway GDP YoY %',
               legend1='NOKJPY',legend2='GDP',
               grid=False,title='NOK vs GDP')


#Now we do our linear regression
x0=pd.concat([df['usd'],df['gbp'],df['eur'],df['brent']],axis=1)
x1=sm.add_constant(x0)
x=x1[x1.index<'2017-04-25']
y=df['nok'][df.index<'2017-04-25']

model=sm.OLS(y,x).fit()
print(model.summary(),'\n')


# In[4]:


#from the summary u can tell there is multicollinearity
#the condition number is skyrocketing
#alternatively, i can use elastic net regression to achieve the convergence
#check the link below for more details
# https://github.com/je-suis-tm/machine-learning/blob/master/coordinate%20descent%20for%20elastic%20net.ipynb
m=en(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10],
     l1_ratio=[.01, .1, .5, .9, .99],  max_iter=5000).fit(x0[x0.index<'2017-04-25'], y)  
print(m.intercept_,m.coef_)


#elastic net estimation results:
#3.79776228406 [ 0.00388958  0.01992038  0.02823187  0.00050092]


# In[5]:


#calculate the fitted value of nok
df['sk_fit']=(df['usd']*m.coef_[0]+df['gbp']*m.coef_[1]+
                 df['eur']*m.coef_[2]+df['brent']*m.coef_[3]+m.intercept_)


# In[6]:


#getting the residual
df['sk_residual']=df['nok']-df['sk_fit']


#one can always argue what if we eliminate some regressors
#in econometrics, if adding extra variables do not decrease adjusted r squared
#or worsen AIC, BIC
#we should include more information as long as it makes sense


# In[7]:


#lets generate signals based on the elastic net
#we set one sigma of the residual as thresholds
#two sigmas of the residual as stop orders
#which is common practise in statistics
upper=np.std(df['sk_residual'][df.index<'2017-04-25'])
lower=-upper

signals=pd.concat([df[i] for i in ['nok', 'usd', 'eur', 'gbp', 'brent', 'sk_fit','sk_residual']], \
                  axis=1)[df.index>='2017-04-25']
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
#unfortunately, there is no johansen test in statsmodels (at the time i wrote this script)
#well, here we go again
#we have to use Engle-Granger two step!
#salute to Engle, mentor of my mentor Gallo
#to the nobel prize winner

#im not gonna explain much here
#if u have checked my other codes, u sould know
#details are in pair trading session
# https://github.com/je-suis-tm/quant-trading/blob/master/Pair%20trading%20backtest.py

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


# In[17]:
#now lets construct a trend following strategy based on the previous strategy
#call it oil money version 2 or whatever
#here i would only import the strategy script as this is a script for analytics and visualization
#the official trading strategy script is in the following link
# https://github.com/je-suis-tm/quant-trading/blob/master/Oil%20Money%20project/Oil%20Money%20Trading%20backtest.py
import oil_money_trading_backtest as om

#generate signals,monitor portfolio performance
#plot positions and total asset
signals=om.signal_generation(dataset,'brent','nok',om.oil_money)
p=om.portfolio(signals,'nok')
om.plot(signals,'nok')
om.profit(p,'nok')

#but thats not enough, we are not happy with the return
#come on, 2 percent return?
#i may as well as deposit the money into the current account 
#and get 0.75% risk free interest rate
#therefore, we gotta try different holding period and stop loss/profit point
#the double loop is very slow, i almost wanna do it in julia
#plz go get a coffee or even lunch and dont wait for it
dic={}
for holdingt in range(5,20):
    for stopp in np.arange(0.3,1.1,0.05):
        signals=om.signal_generation(dataset,'brent','nok',om.oil_money \
                                     holding_threshold=holdingt, \
                                     stop=stopp)
        
        p=om.portfolio(signals,'nok')
        dic[holdingt,stopp]=p['asset'].iloc[-1]/p['asset'].iloc[0]-1
     
profile=pd.DataFrame({'params':list(dic.keys()),'return':list(dic.values())})


# In[18]:

#plotting the distribution of return
#in average the return is 2%
#but we can get -6% and 6% as extreme values
#we dont give a crap about average
#we want the largest positive return

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
profile['return'].apply(lambda x:x*100).hist(histtype='bar', \
                                            color='#f09e8c', \
                                            width=0.45,bins=20)
plt.title('Distribution of Return on NOK Trading')
plt.grid(False)
plt.ylabel('Frequency')
plt.xlabel('Return (%)')
plt.show()


# In[19]:

#plotting the heatmap of return under different parameters
#try to find the optimal parameters to maximize the return

#turn the dataframe into a matrix format first
matrix=pd.DataFrame(columns= \
                    [round(i,2) for i in np.arange(0.3,1.1,0.05)])

matrix['index']=np.arange(5,20)
matrix.set_index('index',inplace=True)

for i,j in profile['params']:
    matrix.at[i,round(j,2)]= \
    profile['return'][profile['params']==(i,j)].item()*100

for i in matrix.columns:
    matrix[i]=matrix[i].apply(float)


#plotting
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(111)
sns.heatmap(matrix,cmap='gist_heat_r',square=True, \
            xticklabels=3,yticklabels=3)
ax.collections[0].colorbar.set_label('Return(%) \n', \
                                     rotation=270)
plt.xlabel('\nStop Loss/Profit (points)')
plt.ylabel('Position Holding Period (days)\n')
plt.title('Profit Heatmap\n',fontsize=10)
plt.style.use('default')

#it seems like the return doesnt depend on the stop profit/loss point
#it is correlated with the length of holding period
#the ideal one should be 9 trading days
#as for stop loss/profit point could range from 0.6 to 1.05
