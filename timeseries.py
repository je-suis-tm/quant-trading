# coding: utf-8



import matplotlib.pyplot as plt 
import statsmodels.api as sm 
import pandas as pd 
import numpy as np 
import random as rd
from sklearn.linear_model import ElasticNetCV as en  
from statsmodels.tsa.stattools import adfuller as adf 
from statsmodels.tsa.seasonal import seasonal_decompose as sd
import copy
from statsmodels.tsa.stattools import grangercausalitytests as gct
from statsmodels.tsa.api import VAR
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing as es


# In[1]: Seasonality


def seasonality_check(df,freq='monthly'):
    
    lag=np.select([freq=='monthly',freq=='quarterly'], \
                      [12,4])
    
    print('ARIMA decomposition')
    
    df2=sd(df,freq=lag)
    print(adf(df))
    sm.graphics.tsa.plot_acf(df)
    plt.show()
    sm.graphics.tsa.plot_pacf(df)
    plt.show()
    df.plot()
    plt.title('original')
    plt.show()
    df2.trend.plot(c=pick_a_color())
    plt.title('trend')
    plt.show()
    df2.seasonal.plot(c=pick_a_color())
    plt.title('seasonality')
    plt.show()
    df2.resid.plot(c=pick_a_color())
    plt.title('residual')
    plt.show()
    
    
    print('HP filter')
    hplag=np.select([freq=='monthly',freq=='quarterly',freq=='annual'], \
                    [14400,1600,100])
    cycle,trend=sm.tsa.filters.hpfilter(df,hplag)
    cycle.plot(c=pick_a_color())
    plt.title('cycle')
    plt.show()
    trend.plot(c=pick_a_color())
    plt.title('trend')
    plt.show() 
    
    print('differential')
    df3=df-df.shift(1)-(df.shift(lag-1)-df.shift(lag))
    df3.plot(c=pick_a_color())
    plt.show()
    
    print('weighted')
    var=locals()
    for i in range(1,lag+1):
        var['seasonal_weight'+str(i)]= \
        np.mean(df[df.index.month==i])/np.mean(df)
        print(var['seasonal_weight'+str(i)])
        
    df_adj=pd.Series(df)
    for j in df.index:
        df_adj[j:j]=df[j:j]/var['seasonal_weight'+str(j.month)]
        
    df_adj.plot(c=pick_a_color())
    plt.show()
    
    
#input value type is pandas series with datetime index
def seasonality(df,n,freq='monthly'):
      
    
    if n==1:
        lag=np.select([freq=='monthly',freq=='quarterly'], \
                      [12,4])
        df2=sd(df,freq=12)
        return df2.trend
    
    elif n==2:
        lag=np.select([freq=='monthly',freq=='quarterly',freq=='annual'], \
                      [14400,1600,100])
        cycle,trend=sm.tsa.filters.hpfilter(df,lag)
        return trend
    
    elif n==3:
        lag=np.select([freq=='monthly',freq=='quarterly'], \
                      [12,4])
        df3=df-df.shift(1)-(df.shift(lag-1)-df.shift(lag))
        return df3
    
    else:
        lag=np.select([freq=='monthly',freq=='quarterly'], \
                      [12,4])
        var=locals()
        df_adj=copy.copy(df)
        
        for i in range(1,lag+1):
            var['seasonal_weight'+str(i)]= \
            np.mean(df[df.index.month==i])/np.mean(df)
            
        for j in df.index:
            df_adj[j:j]=df[j:j]/var['seasonal_weight'+str(j.month)]
        return df_adj


def seasonality_adj(string):
    new=pd.read_csv(string)
    new.set_index(pd.to_datetime(new['date']),inplace=True)
    adj=pd.DataFrame(new['date'])
    del new['date']
    
    new.columns=[i for i in range(len(new.columns))]
    for i in range(len(new.columns)):
        adj[i]=seasonality(new[i],4)
    adj.to_csv('seasonality adj.csv')
    return

    
    
def reverse(df1,df2):
    var=locals()
    for i in range(1,13):
        var['seasonal_weight'+str(i)]= \
        np.mean(df1[df1.index.month==i])/np.mean(df1)
    
    df_adj=copy.copy(df2)
    
    for j in df1.index:
        df_adj[j:j]=df2[j:j]*var['seasonal_weight'+str(j.month)]
        
    return df_adj    
    


# In[2]: OLS and Elastic Net


def OLSregression(y,x,n=0):
    
    x0=sm.add_constant(x)
    m1=sm.OLS(y,x0).fit()
    
    print(m1.summary())
    print(np.std(m1.predict()-np.array(y)))
    
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.plot(y.index,pd.Series(m1.predict()),label='fitted',c=pick_a_color())
    plt.plot(y.index,y,label='actual',c=pick_a_color())

    plt.legend(loc='best')
    plt.title('OLS')
    plt.show()
    
     
    
    
    if n==0:
        return m1.params
    else:
        m2=en(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10],\
              l1_ratio=[.01, .1, .5, .9, .99],  max_iter=5000).fit(x, y)
        print(m2.intercept_,m2.coef_)
        print(np.std(m2.predict(x)-np.array(y)))
        
        fig=plt.figure(figsize=(10,5))
        ax=fig.add_subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.plot(y.index,pd.Series(m2.predict(x)),label='fitted',c=pick_a_color())
        plt.plot(y.index,y,label='actual',c=pick_a_color())
        plt.legend(loc='best')

        plt.title('Elastic Net')
        plt.show()
        
        return [m2.intercept_]+[item for item in m2.coef_]


# In[3]: Holts Winters


def hw_smooth(df,future,lag=12,method='mul'):
    
    forecast=len(df)-1+future    
    
    m=es(df,seasonal=method,trend=method,seasonal_periods=lag,damped=True)
    model=m.fit(optimized=True)
    plt.plot(model.predict(start=0,end=forecast),label='fitted', \
             color=pick_a_color())
    plt.plot(df.index,df,label='actual',color=pick_a_color())
    plt.legend(loc='best')
    plt.show()
    

def hw_forecast(df,future,lag=12,method='mul'):
    
    forecast=len(df)-1+future
    m=es(df,seasonal=method,trend=method,seasonal_periods=lag,damped=True)
    model=m.fit(optimized=True)
    
    return model.predict(start=0,end=forecast)
    
#the csv file should not contain index
def hw_forecast_group(string,future,lag=12,method='mul'):
    
    new=pd.read_csv(string)
    new.set_index(pd.to_datetime(new['date']),inplace=True)
  
    output=pd.DataFrame()
    del new['date']
    
    column=len(new.columns)
    new.columns=[i for i in range(column)]
    temp={}
    for i in range(column):
        
        temp[i]=hw_forecast(new[i],future,lag=12,method='mul')
        output[i]=temp[i]
        
    output.to_csv('forecast.csv')
    

# In[4]: SARIMAX


def SARIMAX(df,future,m=1,n=1,o=1,lag=12,seasonality=True):
    
    print(adf(df.diff().fillna(df.bfill())))
    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(211)
    sm.graphics.tsa.plot_pacf(df,ax=ax)
    bx=fig.add_subplot(212)
    sm.graphics.tsa.plot_acf(df,ax=bx)
    plt.show()
    
    if seasonality==True:
        alpha,beta,gamma=1,1,1
    else:
        alpha,beta,gamma=0,0,0
        
        
    m = sm.tsa.statespace.SARIMAX(df,
                                order=(m, n, o),
                                seasonal_order=(alpha,beta,gamma,lag),
                                enforce_stationarity=False,
                                enforce_invertibility=False).fit()
    
    m.plot_diagnostics(figsize=(20,10))
    print(m.summary())
    
    p=m.get_forecast(steps=future)
    
    fig=plt.figure(figsize=(20,10))
    ax=fig.add_subplot(111)
    ax.plot(p.predicted_mean,label='forecast',c=pick_a_color())
    ax.plot(m.predict().iloc[1:],label='fitted',c=pick_a_color())
    ax.plot(df,label='actual',c=pick_a_color())
    ax.fill_between(p.conf_int().index, \
                    p.conf_int().iloc[:, 0], \
                    p.conf_int().iloc[:, 1], \
                    alpha=.25,color=pick_a_color())
    plt.legend(loc='best')
    plt.title('%s steps ahead forecast'%(future))
    plt.show()


def SARIMAX_forecast(x,future,m=1,n=1,o=1,lag=12,seasonality=True):
    
    if seasonality==True:
        alpha,beta,gamma=1,1,1
    else:
        alpha,beta,gamma=0,0,0
    
    
    a=sm.tsa.statespace.SARIMAX(x,
                                order=(m, n, o),
                                seasonal_order=(alpha,beta,gamma,lag),
                                enforce_stationarity=False,
                                enforce_invertibility=False).fit()
    
    temp=list(a.predict())
    k=a.get_forecast(steps=future).predicted_mean
    
    return temp+(list(k))
    

#the csv file should not contain index
def SARIMAX_forecast_group(string,future,m=1,n=1,o=1,lag=12,seasonality=True):
    
    new=pd.read_csv(string)
    new.set_index(pd.to_datetime(new['date']),inplace=True)
  
    output=pd.DataFrame()
    del new['date']
    
    column=len(new.columns)
    new.columns=[i for i in range(column)]
    temp={}
    for i in range(column):
        
        temp[i]=SARIMAX_forecast(new[i],future,m=1,n=1,o=1,lag=12,seasonality=True)
        output[i]=temp[i]
        
    output.to_csv('forecast.csv')




# In[5]: iteration for finding regressors and best fitted lag

def regression2(y,x):
    
    x0=sm.add_constant(x)
    m1=sm.OLS(y,x0).fit()

    return m1.rsquared


#put y as the first column
def find_x(df):
    
    dictionary={}
    temp=list(df.columns)
    df.columns=[i for i in range(len(df.columns))]

    for k in range(1,len(df.columns)):
        s=regression2(df[0],df[k])
        dictionary[s]=temp[k]
    
    for j in sorted(dictionary.keys())[::-1]:
        print(j,dictionary[j])
    
    
def iteration4(y,x1,x2,x3,x4,n=12):
    perfect={}
    
    for i in range(1,n):
        for j in range(1,n):
            for k in range(1,n):
                for l in range(1,n):
                    para=max(i,j,k,l)
                    temp=regression2(y[para:],pd.concat([x1.shift(i),x2.shift(j),x3.shift(k),x4.shift(l)],axis=1)[para:])
                    if temp not in perfect.keys():
                        perfect[temp]=[i,j,k,l]
                    else:
                        perfect[temp].append([i,j,k,l])
    
    for key in sorted(perfect.keys())[-5:][::-1]:
        print(key,':',perfect[key])
    

def iteration3(y,x1,x2,x3,n=12):
    
    perfect={}
    
    for i in range(1,n):
        for j in range(1,n):
            for k in range(1,n):
                para=max(i,j,k)
                temp=regression2(y[para:],pd.concat([x1.shift(i),x2.shift(j),x3.shift(k)],axis=1)[para:])
                if temp not in perfect.keys():
                    perfect[temp]=[i,j,k]
                else:
                    perfect[temp].append([i,j,k])
    
    for key in sorted(perfect.keys())[-5:][::-1]:
        print(key,':',perfect[key])


def iteration2(y,x1,x2,n=12):
    
    perfect={}
    
    for i in range(1,n):
        for j in range(1,n):
            para=max(i,j)
            temp=regression2(y[para:],pd.concat([x1.shift(i),x2.shift(j)],axis=1)[para:])
            if temp not in perfect.keys():
                perfect[temp]=[i,j]
            else:
                perfect[temp].append([i,j])
    
    for key in sorted(perfect.keys())[-5:][::-1]:
        print(key,':',perfect[key])
        


def iteration1(y,x1,n=12):
    
    perfect={}
    
    for i in range(1,n):
        para=i
        temp=regression2(y[para:],pd.concat([x1.shift(i)],axis=1)[para:])
        if temp not in perfect.keys():
            perfect[temp]=[i]
        else:
            perfect[temp].append([i])
    
    for key in sorted(perfect.keys())[-5:][::-1]:
        print(key,':',perfect[key])



# In[6]: monte carlo


def montecarlo(df,m=58,n=1000):
    x1=sm.add_constant(df.shift(1))
    mo=sm.OLS(df[1:],x1[1:]).fit()

    plt.plot(mo.predict(),label='fitted',c=pick_a_color())
    plt.plot(np.array(df[1:]),label='actual',c=pick_a_color())
    plt.title('AR1')
    plt.legend(loc='best')
    plt.show()
    
    mean,sigma=np.mean(mo.resid),np.std(mo.resid)
    
    keys=[i for i in range(m)]
    values=[[] for i in range(m)]
    sample=dict(zip(keys,values))
    sample[0]=[df[-1] for i in range(n)]
    
    for i in range(n):
        for j in range(1,m):
            e=rd.gauss(mean,sigma)
            temp=sample[j-1][i]*mo.params[1]+mo.params[0]+e
            sample[j].append(temp)
            
    predict=[]

    for j in range(1,m):
        predict.append(np.median(sample[j]))
    
    plt.plot(predict,c=pick_a_color())
    plt.title('Monte Carlo Forecast')
    plt.show()




# In[7]: vector

def vector_check(y,x,n=5):
    print('\nunit root test for regressand\n',adf(y))
    print('\nunit root test for regressor\n',adf(x))
    print('\ngranger causality test\n')
    print('x to y')
    (gct(pd.concat([y,x],axis=1),maxlag=n))
    print('\ny to x')
    (gct(pd.concat([x,y],axis=1),maxlag=n))
    
    print('\n\nEngle-Granger')
    x_sm=sm.add_constant(x)
    m=sm.OLS(y,x_sm).fit()
    print('\n',adf(m.resid))
    
def VAR_IRF(df,n=10,future=20):
    m=VAR(df)
    m.select_order(n)
    n=int(input('order:'))
    model=m.fit(maxlags=n)
    print('\n\n',model.summary())
    model.irf(10).plot()
    
    
# In[8]: convertion
    
#the first column should be date
#input value type is pandas dataframe
    
def quarterly2annual(new):
    
    df=copy.deepcopy(new)
    temp=df.columns
    lag=4
    
    number=len(df.columns)
    df.columns=[i for i in range(number)]
    
    for i in range(1,number):
        df[i+number-1]=df[i].rolling(lag).sum()
 
    data=pd.concat([df.iloc[i,:]for i in range(lag-1,len(df),lag)],axis=1).T
    
    for i in range(1,number):
        del data[i]
        
    data.columns=temp
    
    return data


def monthly2quarterly(new):
    
    df=copy.deepcopy(new)
    temp=df.columns
    lag=3
    
    number=len(df.columns)
    df.columns=[i for i in range(number)]
    
    for i in range(1,number):
        df[i+number-1]=df[i].rolling(lag).sum()
 
    data=pd.concat([df.iloc[i,:]for i in range(lag-1,len(df),lag)],axis=1).T
    
    for i in range(1,number):
        del data[i]
        
    data.columns=temp
    
    return data


def ytd2monthly(new):
    
    df=copy.deepcopy(new)
    temp=df.columns
    df.set_index(pd.to_datetime(df[str(df.columns[0])]),inplace=True)
    
    number=len(df.columns)
    df.columns=[i for i in range(number)]
    
    for i in range(1,number):
        df[i+number-1]=df[i].diff()

        for j in range(len(df)):
            if df.index[j].month==1:
                df.set_value(df.index[j],i+number-1,df[i].iloc[j])
      
        del df[i]
    
  
    df.columns=temp
    df.reset_index(inplace=True,drop=True)
    
        
    return df


def ytd2annual(new):
    
    df=copy.deepcopy(new)

    df.set_index(pd.to_datetime(df[str(df.columns[0])]),inplace=True)
    
    output=df[df.index.month==12]
    output.reset_index(inplace=True)
    
    return output

    
# In[9]: plotting

#heat map
#set df date as index before passing to this function
#note that fig_size is in scale with fontsize
def heatmap(df,fig_size=(10,5),fontsize=1):
    
    temp=df.corr()
    
    fig=plt.figure(figsize=fig_size)
    ax=fig.add_subplot(111)

    sns.set(font_scale=fontsize)
    
    mask = np.zeros_like(temp)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(temp, xticklabels=temp.columns, \
                yticklabels=temp.columns, annot=True, \
                mask=mask, ax=ax)
    
    sns.set()
    
    
#set df date as index before passing to this function
def plot_all(df,color='b'):
    
    for i in df.columns:
        print(i)
        df[i].plot(c=color)
        plt.show()



def pick_a_color():
    
    colorlist= \
    ['#F8B195',
     '#F67280',
     '#C06C84',
     '#6C5B7B',
     '#355C7D',
     '#99B898',
     '#FECEAB',
     '#FF847C',
     '#E84A5F',
     '#2A363B',
     '#A8E6CE',
     '#DCEDC2',
     '#FFD3B5',
     '#FFAAA6',
     '#FF8C94',
     '#A8A7A7',
     '#CC527A',
     '#E8175D',
     '#474747',
     '#363636',
     '#A7226E',
     '#EC2049',
     '#F26B38',
     '#F7DB4F',
     '#2F9599',
     '#E1F5C4',
     '#EDE574',
     '#F9D423',
     '#FC913A',
     '#FF4E50',
     '#E5FCC2',
     '#9DE0AD',
     '#45ADA8',
     '#547980',
     '#594F4F',
     '#FE4365',
     '#FC9D9A',
     '#F9CDAD',
     '#C8C8A9',
     '#83AF9B',
     '#BCE784',
     '#5DD39E']
    
    a=rd.randint(0,39)
    
    return colorlist[a]