
# coding: utf-8

# In[1]:


import numpy as np
import os
import pandas as pd
import scipy.optimize
import random as rd
import matplotlib.pyplot as plt
import cvxopt
os.chdir('H:/')


# ### define functions

# In[2]:


#etl
def prepare(grand):
    
    global D
    D={}
    
    for i in grand['Year'].unique():
        D[i]=grand[grand['Year']==i]
        D[i].reset_index(inplace=True,drop=True)
        
    return D


# In[3]:


#quadratic programming
def get_ans(quadratic_coeff,linear_coeff,inequality_coeff,
           inequality_value,equality_coeff,equality_value):

    cvxopt.solvers.options['show_progress']=False

    ans=cvxopt.solvers.qp(P=quadratic_coeff,q=linear_coeff,
                          G=inequality_coeff,h=inequality_value,
                          A=equality_coeff,b=equality_value)['x']
    
    return list(ans)


# In[4]:


#linear version
def get_production(initial_guess):
    
    #create profit
    price=D[currentyear]['price']
    linear_coeff=cvxopt.matrix(initial_guess-price)

    #none
    quadratic_coeff=cvxopt.matrix(0.0,(len(D[currentyear]),len(D[currentyear])))

    #maximum cropland constraint
    equality_coeff=cvxopt.matrix(D[currentyear]['yield_i']).T
    equality_value=cvxopt.matrix(malay_land['Value'][malay_land['Year']==currentyear].item()*1000)

    #crop rotation constraint
    area_hist=D[currentyear-1]['area'].tolist()
    eco_lifespan=D[currentyear]['eco lifespan'].tolist()

    inequality_coeff=cvxopt.matrix(0.0,(len(D[currentyear]),len(D[currentyear])))

    #diagonal matrix
    #use -1 to achieve larger than
    inequality_coeff[::len(D[currentyear])+1]=D[currentyear]['yield_i'].apply(lambda x:-1*x).tolist()

    #use -1 to achieve larger than
    inequality_value=cvxopt.matrix(np.multiply(np.multiply(area_hist,eco_lifespan),-1))
    
    #cvxopt
    estimate=get_ans(quadratic_coeff,linear_coeff,inequality_coeff,
           inequality_value,equality_coeff,equality_value)
    
    
    return estimate


# In[5]:


#quadratic version
def get_production(initial_guess):
    
    #get historical price
    price_hist=np.mat(D[currentyear-1]['price']).T

    #create alpha diagonal
    alpha=np.diag(D[currentyear]['alpha'])

    #get historical production
    #use negative value
    production_hist=np.mat(D[currentyear-1]['production']).T

    #get population change
    delta_pop=malay_pop['Value'][malay_pop['Year']==currentyear].item()-malay_pop['Value'][malay_pop['Year']==currentyear-1].item()

    #create beta
    beta=np.mat(D[currentyear]['beta']).T

    #get gdp per capita change
    delta_gdp=malay_gdp['Value'][malay_gdp['Year']==currentyear].item()-malay_gdp['Value'][malay_gdp['Year']==currentyear-1].item()

    #create gamma
    gamma=np.mat(D[currentyear]['gamma']).T

    #create linear coefficient
    #production_hist*-1 to obtain negative production
    linear_coeff=-price_hist+(alpha*production_hist*-1)-delta_pop*beta-delta_gdp*gamma+np.mat(initial_guess).T
    linear_coeff=cvxopt.matrix(linear_coeff)

    #create quadratic coefficient
    quadratic_coeff=cvxopt.matrix(alpha)

    #maximum cropland constraint
    equality_coeff=cvxopt.matrix(D[currentyear]['yield_i']).T
    equality_value=cvxopt.matrix(malay_land['Value'][malay_land['Year']==currentyear].item()*1000)

    #crop rotation constraint seems to be too large for upper bound
    #we use the same upperbound as perennial
    area_hist=D[currentyear-1]['area']
    eco_lifespan=D[currentyear]['eco lifespan'].tolist()
    
    #smaller than
    upperblock=np.diag(D[currentyear]['yield_i'])

    #larger than
    #use -1
    lowerblock=np.diag(D[currentyear]['yield_i'].apply(lambda x:-1*x))

    #concat
    inequality_coeff=cvxopt.matrix(np.append(upperblock,lowerblock,axis=0))
    inequality_value=cvxopt.matrix((area_hist*upperbound).append(np.multiply(np.multiply(area_hist,eco_lifespan),-1)))
    
    #cvxopt
    estimate=get_ans(quadratic_coeff,linear_coeff,inequality_coeff,
               inequality_value,equality_coeff,equality_value)


    return estimate


# In[6]:


#compute sse
def costfunction(initial_guess):
    
    #cvxopt
    estimate=get_production(initial_guess)
    
    actual=D[currentyear]['production'].tolist()
    
    cost=sum(np.power(np.divide(np.subtract(actual,estimate),actual),2))
    
    return cost


# In[7]:


#least square to estimate the best cost
def ls_estimate(initial_guess,diagnosis=True):

    if diagnosis:
        #get sse before least square
        sse_original=costfunction(initial_guess)
        print(f'Initial SSE: {round(sse_original,2)}')
    
    #least square
    least_square=scipy.optimize.minimize(costfunction,
                                         x0=(initial_guess),
                                         method='Nelder-Mead')
    
    #if successful return result
    #else print the issue
    if least_square.success:               

        if diagnosis:
            sse=costfunction(least_square.x)
            print(f'Result SSE: {round(sse,2)}')

        return least_square.x
    
    else:
        
        print(least_square)

        return [0]


# In[8]:


#using random initial value to find the best starting point
def find_init(num=10):
    
    global currentyear
    
    dic={}
    
    #try random cost
    for _ in range(num):

        initial_guess=pd.Series([i*rd.random() for i in D[currentyear]['price']])

        ans=ls_estimate(initial_guess,diagnosis=False)
        
        if len(ans)>1:
            
            sample=[]
            
            #get average sse of all years
            for currentyear in range(beginyear,endyear):
                          
                cost=costfunction(ans)
                sample.append(cost)
            
            dic[np.mean(sample)]=initial_guess
        
        
    return dict(sorted(dic.items()))


# In[9]:


#write init values into txt
def write_file(dic):
    
    f=open('init.txt','w')

    for i in dic:
        f.write('\n\n'+str(i)+'\n\n')
        for j in dic[i].astype(str):
            f.write(j+'\n')

    f.close()
    
    return


# In[10]:


#use production to compute price
def compute_price(production):
    
    #get historical price
    price_hist=np.mat(D[currentyear-1]['price']).T

    #create alpha diagonal
    alpha=np.diag(D[currentyear]['alpha'])

    #get historical production
    #use negative value
    production_hist=np.mat(D[currentyear-1]['production']).T

    #get population change
    delta_pop=malay_pop['Value'][malay_pop['Year']==currentyear].item()-malay_pop['Value'][malay_pop['Year']==currentyear-1].item()

    #create beta
    beta=np.mat(D[currentyear]['beta']).T

    #get gdp per capita change
    delta_gdp=malay_gdp['Value'][malay_gdp['Year']==currentyear].item()-malay_gdp['Value'][malay_gdp['Year']==currentyear-1].item()

    #create gamma
    gamma=np.mat(D[currentyear]['gamma']).T
    
    #predict price
    price_est=price_hist+delta_pop*beta+delta_gdp*gamma-(alpha*production*-1)+(alpha*production_hist*-1)
    
    return price_est.ravel().tolist()[0]


# ### execution

# In[11]:


grand=pd.read_csv('tres_grand.csv')

capita=pd.read_csv('capita.csv')


# In[12]:


#create time series
capita.set_index('Date',inplace=True,)

capita.index=pd.to_datetime(capita.index)


# In[13]:


global malay_land
malay_land=pd.read_csv('malay_land.csv')

global malay_pop
malay_pop=pd.read_csv('malay_pop.csv')

global malay_gdp
malay_gdp=pd.read_csv('malay_gdp.csv')


# In[14]:


#ffill land area for 2018
malay_land.at[6,'Value']=malay_land.at[5,'Value']


# In[15]:


global D
D=prepare(grand)


# In[16]:


global beginyear,endyear
beginyear=2013
endyear=2019


# In[17]:


global currentyear
currentyear=2013


# In[18]:


global upperbound,lowerbound
upperbound=1.2
lowerbound=-0.8


# ### margin weighted cost

# In[19]:


cost_optimal=[46.45261724887184,
 25.771497795481803,
 8.04132847940984,
 257.7585247333969,
 6.2550124573415955,
 0.286864009247044,
 79.32795295554159,
 14.445506332549158,
 1.685693777638147,
 1.7429878194147876,
 1.1023982955265745,
 8.870826525406954,
 10.129836899368781,
 12.685177915888149,
 13825.333042426462,
 27.911072146085953,
 6.803152547546634,
 2.218450015909855,
 8.289956670382614,
 4.143929068809526,
 50.592542452998224,
 4.215768472073825,
 371.2574670551623,
 106.12409983634397,
 8.127574487076723,
 5.49462574257295,
 6.734987344270521,
 0.25431612106271956,
 25.95233336898883,
 27.02920135710488]


# In[20]:


# #cost linear system
# def cost_func(x):
    
#     temp=[None for _ in range(len(x))]
#     for i in range(len(x)):
#         temp[i]=ss[i]*tt-ss[i]*sum(x)-x[i]
    
#     return temp

# #create margin weighted cost
# dick={}

# for currentyear in range(beginyear,endyear):
    
#     global ss
#     ss=D[currentyear]['production']/sum(D[currentyear]['production'])

#     global tt
#     tt=sum(D[currentyear]['price'])

#     dick[currentyear]=scipy.optimize.fsolve(cost_func,x0=[1000 for _ in range(len(ss))])

# #get average cost
# avgcost=[]
# for ii in range(len(ss)):
#     avgcost.append(np.mean([dick[i][ii] for i in dick]))


# ### viz

# In[21]:


#get predicted production
X={}

for currentyear in range(beginyear,endyear):
        
    x=get_production(cost_optimal)
    X[currentyear]=x

#plot predicted production
for ii in range(len(X[currentyear])):
    
    Y=[D[i]['production'][ii] for i in range(beginyear,endyear)]

    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.plot(range(beginyear,endyear),[X[i][ii] for i in X],label='Est',color='#ef6466')
    plt.plot(range(beginyear,endyear),Y,label='Act',color='#9f65a2')
    plt.ylabel('Tonnes')
    plt.xlabel('Year')
    plt.legend()
    plt.title(D[currentyear]['Item'][ii]+' Production')
    plt.show()

#plot overall production
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.plot(range(beginyear,endyear),[sum(X[i]) for i in X],
         label='Est',color='#ef6466')
plt.plot(range(beginyear,endyear),[sum(D[i]['production']) for i in X],
         label='Act',color='#9f65a2')
plt.ylabel('Tonnes')
plt.xlabel('Year')
plt.legend()
plt.title('Overall Production')
plt.show()


# In[22]:


#plot predicted price
price_predict={}
for currentyear in range(beginyear,endyear):
    
    price_predict[currentyear]=compute_price(np.mat(X[currentyear]).T)

#plot predicted price
for ii in range(len(price_predict[currentyear])):
    
    Y=[D[i]['price'][ii] for i in range(beginyear,endyear)]

    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.ylabel('USD/Tonnes')
    plt.xlabel('Year')
    plt.plot(range(beginyear,endyear),[price_predict[i][ii] for i in price_predict],
             label='Est',color='#99B800',)
    plt.plot(range(beginyear,endyear),Y,label='Act',color='#1b5004',)
    plt.legend()
    plt.title(D[currentyear]['Item'][ii]+' Price')
    plt.show()


# ### forecast

# In[23]:


beginyear=2019;endyear=2025


# In[24]:


#add gdp per capita forecast from imf
gdp_extra=malay_gdp.iloc[:(endyear-beginyear)].copy()

gdp_extra['Year']=range(beginyear,endyear)
gdp_extra['Year Code']=range(beginyear,endyear)

gdp_extra['Value']=capita['Mid Price'][str(beginyear):str(endyear)].tolist()

malay_gdp=malay_gdp.append(gdp_extra)


# In[25]:


#add land per capita forecast
#i mean ffill
land_extra=malay_land.iloc[:(endyear-beginyear)].copy()

land_extra['Year']=range(beginyear,endyear)
land_extra['Year Code']=range(beginyear,endyear)


# In[26]:


#assume land grows 1% per annum
temp=[malay_land['Value'].iloc[-1]]
for i in range(len(land_extra)):
    temp.append(temp[-1]*1.01)

temp.pop(0)


# In[27]:


#concat land
land_extra['Value']=temp

malay_land=malay_land.append(land_extra)


# In[28]:


#make forecast
for currentyear in range(beginyear,endyear):

    D[currentyear]=D[currentyear-1].copy()
    D[currentyear]['production']=0.0
    D[currentyear]['area']=0.0
    D[currentyear]['price']=0.0
    D[currentyear]['Year']=currentyear
    
    D[currentyear]['production']=get_production(cost_optimal)
    D[currentyear]['price']=compute_price(np.mat(D[currentyear]['production']).T)
    D[currentyear]['area']=np.multiply(D[currentyear]['production'],D[currentyear]['yield_i'])


# In[29]:


#plot predicted production
for ii in range(len(D[currentyear])):
    
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.ylabel('Tonnes')
    plt.xlabel('Year')
    plt.plot([D[i]['production'][ii] for i in D],color='#0e3c6b',)
    plt.title(D[currentyear]['Item'][ii]+' Production')
    plt.show()

#plot overall production
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.ylabel('Tonnes')
plt.xlabel('Year')
plt.plot([sum(D[i]['production']) for i in D],color='#0e3c6b',)
plt.title('Overall Production')
plt.show()


# In[30]:


#plot predicted price
for ii in range(len(D[currentyear])):
    
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.ylabel('USD/Tonnes')
    plt.xlabel('Year')
    plt.plot([D[i]['price'][ii] for i in D],color='#7d0b02',)
    plt.title(D[currentyear]['Item'][ii]+' Price')
    plt.show()


# In[31]:


#export forecast
pd.concat([D[i] for i in range(beginyear,endyear)]).to_csv('forecast.csv',index=False)

