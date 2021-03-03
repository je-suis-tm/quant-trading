
# coding: utf-8

# In[1]:


import numpy as np
import os
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import cvxopt
os.chdir('H:/')


# ### define functions

# In[2]:


#create xy for least square
def create_xy(target_crop,grande,malay_gdp,malay_pop):
    
    y=grande['price'][target_crop]

    x=pd.concat([malay_gdp['Value'],malay_pop['Value'],
                       grande['production'][target_crop]],axis=1)

    x=sm.add_constant(x)
    
    #set production negative
    x[target_crop.lower()]=x[target_crop].apply(lambda x:-1*x)
    del x[target_crop]
    
    return x,y


# In[3]:


#linear regression
def lin_reg(crops,grande,malay_gdp,malay_pop,viz=False):

    D={}
    
    #run regression
    for target_crop in crops:
        
        #create xy
        x,y=create_xy(target_crop,grande,malay_gdp,malay_pop)
        
        m=sm.OLS(y,sm.add_constant(x)).fit()

        D[target_crop]=(m.rsquared,m.params.tolist())
        
        #viz
        if viz:
            fig=plt.figure(figsize=(10,5))
            ax=fig.add_subplot(111)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.ylabel('USD/Tonnes')
            plt.xlabel('Year')
            plt.plot(range(beginyear,endyear),m.predict(),label='Est',color='#C8C8A9')
            plt.plot(range(beginyear,endyear),y,label='Act',color='#EDE574')
            plt.title(target_crop+' Price')
            plt.legend()
            plt.show()

    return D


# In[4]:


def constrained_ols(x,y):

    linear_coeff=cvxopt.matrix(-1*np.mat(y.tolist())*np.mat(x)).T
    quadratic_coeff=cvxopt.matrix(np.mat(x).T*np.mat(x))

    #inequality constraint
    inequality_coeff=cvxopt.matrix(0.0,(len(x.columns),len(x.columns)))

    #diagonal matrix
    #use -1 to achieve larger than
    inequality_coeff[::len(x.columns)+1]=-1
    
    #no constraint for the constant
    inequality_coeff[0,0]=0
    inequality_value=cvxopt.matrix([0.0 for _ in range(len(x.columns))])

    cvxopt.solvers.options['show_progress']=False

    ans=cvxopt.solvers.qp(P=quadratic_coeff,q=linear_coeff,
                          G=inequality_coeff,h=inequality_value)['x']
    
    return ans


# In[5]:


#create params by using constrained ols
def get_params(crops,grande,malay_gdp,malay_pop,viz=False):
    
    D={}
    
    for target_crop in crops:

        #create xy
        x,y=create_xy(target_crop,grande,malay_gdp,malay_pop)

        #constrained ols
        ans=constrained_ols(x,y)

        #viz
        if viz:

            #get forecast and convert to list
            forecast=np.mat(ans).T*np.mat(x).T
            forecast=forecast.ravel().tolist()[0]
            fig=plt.figure(figsize=(10,5))
            ax=fig.add_subplot(111)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.ylabel('USD/Tonnes')
            plt.xlabel('Year')
            plt.plot(range(beginyear,endyear),forecast,label='Est',color='#C8C8A9',)
            plt.plot(range(beginyear,endyear),y,label='Act',color='#EDE574')
            plt.legend()
            plt.title(target_crop+' Price')
            plt.show()

        D[target_crop]=list(ans)
        
    return D


# ### execution

# In[6]:


global beginyear,endyear
beginyear=2012
endyear=2019


# In[7]:


grand=pd.read_csv('grand.csv')

malay_pop=pd.read_csv('malay_pop.csv')

malay_gdp=pd.read_csv('malay_gdp.csv')


# In[8]:


#cleanse
malay_pop=malay_pop[malay_pop['Year'].isin(range(beginyear,endyear))]
malay_pop.reset_index(inplace=True,drop=True)


# In[9]:


#pivot
grande=grand.pivot(index='Year',columns='Item',values=['price','production'])
grande.reset_index(inplace=True,drop=True)


# In[10]:


#find crops
crops=grande.columns.levels[1]


# ### linear regression

# In[11]:


D1=lin_reg(crops,grande,malay_gdp,malay_pop,viz=True)


# In[12]:


D1


# ### constrained regression

# In[13]:


D2=get_params(crops,grande,malay_gdp,malay_pop,viz=True)


# In[14]:


# #replace unsuccessful result with ols
# for i in D2:
#     if len([j for j in D2[i] if j<0])>0:
#         D2[i]=D1[i][1]        


# In[15]:


#create output
output=pd.DataFrame(columns=D2.keys())

for i in D2:
    output[i]=D2[i]

output=output.T

output.columns=['constant','gamma','beta','alpha']

output.index.name='Item'

output.reset_index(inplace=True)


# In[16]:


#merge with grand
tres_grand=grand.merge(output,on='Item',how='left')

tres_grand.to_csv('tres_grand.csv',index=False)


# ### backtest

# In[17]:


forecast=pd.read_csv('forecast.csv')


# In[18]:


#extract historical generic 1st
palm=pd.read_csv('palm.csv')
palm.set_index('Date',inplace=True,)
palm.index=pd.to_datetime(palm.index)
palm.columns=['Palm oil','Rubber1','Rubber2']


# In[19]:


cme=pd.read_csv('cme.csv')

#extract cme palm oil futures 
palm_futures=cme[cme['date']==cme['date'].iloc[-1]][cme['product_id']==2457]

palm_futures=palm_futures[['expiration_date','prior_settle']]
palm_futures.columns=['Date','Palm oil']

palm_futures.set_index('Date',inplace=True)
palm_futures.index=pd.to_datetime(palm_futures.index)


# In[20]:


#concat, currency convert and get annual avg
temp=palm['Palm oil'][str(beginyear):].apply(lambda x:x*0.23).append(palm_futures['Palm oil'][:str(endyear+5)])

palmoil=temp.resample('1A').mean()

#convert datetime index from year end to beginning
palmoil.index=[pd.to_datetime(str(i)[:5]+'01-01') for i in palmoil.index]


# In[21]:


#create oil palm actual and estimated price
oilpalm_act=grand['price'][grand['Item']=='Oil palm fruit']
oilpalm_act.reset_index(inplace=True,drop=True)

oilpalm_est=oilpalm_act.iloc[-1:].append(forecast['price'][forecast['Item']=='Oil palm fruit'])
oilpalm_est.reset_index(inplace=True,drop=True)


# In[22]:


#dual axis plot
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(111)


ax.set_xlabel('Date')
ax.set_ylabel('Palm Oil Generic 1st',color='#45ADA8')
ax.plot(palmoil.index,palmoil,color='#45ADA8',label='Palm Oil')
ax.tick_params(axis='y',labelcolor='#45ADA8')
ax.yaxis.labelpad=15

plt.legend(loc=3)
ax2=ax.twinx()

ax2.set_ylabel('Oil Palm Fruit Price',color='#EC2049',rotation=270)
ax2.plot(palmoil.index[:len(oilpalm_act)],oilpalm_act,
         color='#EC2049',label='Oil Palm Act')
ax2.plot(palmoil.index[len(oilpalm_est)-1:],oilpalm_est,
         color='#fea5c4',label='Oil Palm Est',linestyle='-.')
ax2.tick_params(axis='y',labelcolor='#EC2049')
ax2.yaxis.labelpad=15

fig.tight_layout()
plt.legend(loc=4)
plt.grid(False)
plt.title('Palm Oil vs Oil Palm')
plt.show()

