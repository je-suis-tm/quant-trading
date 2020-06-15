
# coding: utf-8

# In[1]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
os.chdir('k:/')


# In[2]:

#plot two curves on same x axis, different y axis
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
    ax2=ax.twinx()

    ax2.set_ylabel(y_label2, color=sec_color,rotation=270)
    ax2.plot(xaxis, data2, color=sec_color,label=legend2)
    ax2.tick_params(axis='y',labelcolor=sec_color)
    ax2.yaxis.labelpad=15

    fig.tight_layout()
    plt.legend(loc=4)
    plt.grid(grid)
    plt.title(title)
    plt.show()



# In[3]:

#read dataframe    
df=pd.read_csv('vas crude copaud.csv',encoding='utf-8')
df.set_index('date',inplace=True)
df.index=pd.to_datetime(df.index)


# In[4]:

#run regression on each input

D={}

for i in df.columns:
    if i!='cop':
            x=sm.add_constant(df[i])
            y=df['cop']
            m=sm.OLS(y,x).fit()
            D[i]=m.rsquared
            
D=dict(sorted(D.items(),key=lambda x:x[1],reverse=True))


# In[5]:

#create r squared bar charts

colorlist=[]

for i in D:
    if i =='wti':
        colorlist.append('#447294')
    elif i=='brent':
        colorlist.append('#8fbcdb')
    elif i=='vasconia':
        colorlist.append('#f4d6bc')
    else:
        colorlist.append('#cdc8c8')
        
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

width=0.7

for i in D:
    plt.bar(list(D.keys()).index(i)+width,            
            D[i],width=width,label=i,
            color=colorlist[list(D.keys()).index(i)])
 
plt.title('Regressions on COP')
plt.ylabel('R Squared\n')
plt.xlabel('\nRegressors')
plt.xticks(np.arange(len(D))+width,
           [i.upper() for i in D.keys()],fontsize=8)
plt.show()


# In[6]:

#normalized value of wti,brent and vasconia
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['vasconia']/df['vasconia'].iloc[0]).plot(c='#6f6ff4',
                                             label='Vasconia',alpha=0.5)
(df['brent']/df['brent'].iloc[0]).plot(c='#e264c0',
                                   label='Brent',alpha=0.5)
(df['wti']/df['wti'].iloc[0]).plot(c='#fb6630',
                                   label='WTI',alpha=0.5)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Crude Oil Blends')
plt.show()


# In[7]:

#cop vs gold
dual_axis_plot(df.index,df['cop'],df['gold'],
               x_label='Date',y_label1='Colombian Peso',
               y_label2='Gold LBMA',
               legend1='COP',
               legend2='Gold',
               title='COP VS Gold',
               fst_color='#96CEB4',sec_color='#FFA633')

#cop vs usd
dual_axis_plot(df.index,df['cop'],df['usd'],
               x_label='Date',y_label1='Colombian Peso',
               y_label2='US Dollar',
               legend1='COP',
               legend2='USD',
               title='COP VS USD',
               fst_color='#9DE0AD',sec_color='#5C4E5F')


# In[8]:

#cop vs brl
dual_axis_plot(df.index,df['cop'],df['brl'],
               x_label='Date',y_label1='Colombian Peso',
               y_label2='Brazilian Real',
               legend1='COP',
               legend2='BRL',
               title='COP VS BRL',
               fst_color='#a4c100',sec_color='#f7db4f')

#usd vs mxn
dual_axis_plot(df.index,df['usd'],df['mxn'],
               x_label='Date',y_label1='US Dollar',
               y_label2='Mexican Peso',
               legend1='USD',
               legend2='MXN',
               title='USD VS MXN',
               fst_color='#F4A688',sec_color='#A2836E')

#cop vs mxn
dual_axis_plot(df.index,df['cop'],df['mxn'],
               x_label='Date',y_label1='Colombian Peso',
               y_label2='Mexican Peso',
               legend1='COP',
               legend2='MXN',
               title='COP VS MXN',
               fst_color='#F26B38',sec_color='#B2AD7F')


# In[9]:

#cop vs vasconia
dual_axis_plot(df.index,df['cop'],df['vasconia'],
               x_label='Date',y_label1='Colombian Peso',
               y_label2='Vasconia Crude',
               legend1='COP',
               legend2='Vasconia',
               title='COP VS Vasconia',
               fst_color='#346830',sec_color='#BBAB9B')


# In[10]:

#create before/after regression comparison
m=sm.OLS(df['cop'][:'2016'],sm.add_constant(df['vasconia'][:'2016'])).fit()
before=m.rsquared
m=sm.OLS(df['cop']['2017':],sm.add_constant(df['vasconia']['2017':])).fit()
after=m.rsquared

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.bar(['Before 2017',
         'After 2017'],
        [before,after],color=['#82b74b', '#5DD39E'])
plt.ylabel('R Squared')
plt.title('Before/After Regression')
plt.show()


# In[11]:


#create 1 std, 2 std band before 2017
x_train,x_test,y_train,y_test=train_test_split(
        sm.add_constant(df['vasconia'][:'2016']),
        df['cop'][:'2016'],test_size=0.5,shuffle=False)
    
m=sm.OLS(y_test,x_test).fit()
    
forecast=m.predict(x_test)
    
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
forecast.plot(label='Fitted',c='#FEFBD8')
y_test.plot(label='Actual',c='#ffd604')
ax.fill_between(y_test.index,
                    forecast+np.std(m.resid),
                    forecast-np.std(m.resid),
                    color='#F4A688', 
                    alpha=0.6, 
                    label='1 Sigma')
    
ax.fill_between(y_test.index,
                    forecast+2*np.std(m.resid),
                    forecast-2*np.std(m.resid),
                    color='#8c7544', 
                    alpha=0.8, 
                    label='2 Sigma')
    
plt.legend(loc=0)
plt.title(f'Colombian Peso Positions\nR Squared {round(m.rsquared*100,2)}%\n')
plt.xlabel('\nDate')
plt.ylabel('COPAUD')
plt.show()


# In[12]:


#create 1 std, 2 std band after 2017
x_train,x_test,y_train,y_test=train_test_split(
        sm.add_constant(df['vasconia']['2017':]),
        df['cop']['2017':],test_size=0.5,shuffle=False)
    
m=sm.OLS(y_test,x_test).fit()
    
forecast=m.predict(x_test)
    
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
forecast.plot(label='Fitted',c='#FEFBD8')
y_test.plot(label='Actual',c='#ffd604')
ax.fill_between(y_test.index,
                    forecast+np.std(m.resid),
                    forecast-np.std(m.resid),
                    color='#F4A688', 
                    alpha=0.6, 
                    label='1 Sigma')
    
ax.fill_between(y_test.index,
                    forecast+2*np.std(m.resid),
                    forecast-2*np.std(m.resid),
                    color='#8c7544', \
                    alpha=0.8, \
                    label='2 Sigma')
    
plt.legend(loc=0)
plt.title(f'Colombian Peso Positions\nR Squared {round(m.rsquared*100,2)}%\n')
plt.xlabel('\nDate')
plt.ylabel('COPAUD')
plt.show()


# In[13]:

#shrink data size for better viz
dataset=df['2016':]
dataset.reset_index(inplace=True)


# In[14]:

#import the strategy script as this is a script for analytics and visualization
#the official trading strategy script is in the following link
# https://github.com/je-suis-tm/quant-trading/blob/master/Oil%20Money%20project/Oil%20Money%20Trading%20backtest.py
import oil_money_trading_backtest as om

#generate signals,monitor portfolio performance
#plot positions and total asset
signals=om.signal_generation(dataset,'vasconia','cop',om.oil_money,stop=0.001)
p=om.portfolio(signals,'cop')
om.plot(signals,'cop')
om.profit(p,'cop')


# In[15]:


#try different holding period and stop loss/profit point
dic={}
for holdingt in range(5,20):
    for stopp in np.arange(0.001,0.005,0.0005):
        signals=om.signal_generation(dataset,'vasconia','cop',om.oil_money,
                                     holding_threshold=holdingt,
                                     stop=round(stopp,4))
        
        p=om.portfolio(signals,'cop')
        dic[holdingt,round(stopp,4)]=p['asset'].iloc[-1]/p['asset'].iloc[0]-1
     
profile=pd.DataFrame({'params':list(dic.keys()),'return':list(dic.values())})


# In[16]:


#plotting the distribution of return
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
profile['return'].apply(lambda x:x*100).hist(histtype='bar',
                                             color='#b2660e',
                                             width=0.45,bins=20)
plt.title('Distribution of Return on COP Trading')
plt.grid(False)
plt.ylabel('Frequency')
plt.xlabel('Return (%)')
plt.show()


# In[17]:


#plotting the heatmap of return under different parameters
#try to find the optimal parameters to maximize the return

#convert the dataframe into a matrix format first
matrix=pd.DataFrame(columns=[round(i,4) for i in np.arange(0.001,0.005,0.0005)])

matrix['index']=np.arange(5,20)
matrix.set_index('index',inplace=True)

for i,j in profile['params']:
    matrix.at[i,round(j,4)]=     profile['return'][profile['params']==(i,j)].item()*100

for i in matrix.columns:
    matrix[i]=matrix[i].apply(float)


#plotting
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(111)
sns.heatmap(matrix,cmap=plt.cm.viridis,
            xticklabels=3,yticklabels=3)
ax.collections[0].colorbar.set_label('Return(%)\n',
                                      rotation=270)
plt.xlabel('\nStop Loss/Profit (points)')
plt.ylabel('Position Holding Period (days)\n')
plt.title('Profit Heatmap\n',fontsize=10)
plt.style.use('default')

#it seems like the return doesnt depend on the stop profit/loss point
#it is correlated with the length of holding period
#the ideal one should be 17 trading days
#as for stop loss/profit point could range from 0.002 to 0.005

