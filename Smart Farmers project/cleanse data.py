
# coding: utf-8

# In[1]:


import os
os.chdir('H:/')
import pandas as pd
import numpy as np


# ### define functions

# In[2]:


#etl
def prepare(target_land,target_prod,target_prix):

    #land clean up
    target_land=target_land[['Year','Value']].copy()

    #prix clean up
    target_prix=target_prix[['Item','Year','Value']].copy()

    #create area and clean up
    target_area=target_prod[target_prod['Element']=='Area harvested'].copy()

    target_area=target_area[['Item','Year','Value','type','lifespan']].copy()

    #production clean up
    target_prod=target_prod[target_prod['Element']=='Production'].copy()

    target_prod=target_prod[['Item','Year','Value','class']].copy()

    #compute yield inverse and clean up
    target_yield_inverse=target_prod.merge(target_area,on=['Item','Year'],how='left')

    target_yield_inverse['Value']=np.divide(target_yield_inverse['Value_y'],target_yield_inverse['Value_x'])

    target_yield_inverse=target_yield_inverse[['Item', 'Year','Value','type', 'lifespan']]

    #sort by item and year
    for data in [target_prod,target_area,target_prix,target_yield_inverse]:
        data.sort_values(['Item','Year'],inplace=True)

    #concatenate
    global D
    D={}

    for currentyear in range(beginyear,endyear):   

        temp1=target_prod[target_prod['Year']==currentyear].merge(
        target_area[target_area['Year']==currentyear],on=['Item', 'Year'],how='outer')
        temp2=target_prix[target_prix['Year']==currentyear].merge(
        target_yield_inverse[target_yield_inverse['Year']==currentyear],on=['Item', 'Year'],how='outer')

        temp1.columns=temp1.columns.str.replace('Value_x','production')
        temp1.columns=temp1.columns.str.replace('Value_y','area')
        temp2.columns=temp2.columns.str.replace('Value_x','price')
        temp2.columns=temp2.columns.str.replace('Value_y','yield_i')

        data=temp1.merge(temp2,on=['Item', 'Year', 'type', 'lifespan'],how='outer')

        D[currentyear]=data                
    
    #compute eco lifespan for perennials
    for currentyear in range(beginyear,endyear):
        
        eco_lifespan=[default_discount for _ in range(len(D[currentyear]))]
        indices=D[currentyear]['lifespan'].dropna().index
        perennial=D[currentyear]['lifespan'].dropna().apply(lambda x:(x*eco_coeff-1)/(x*eco_coeff))

        for i in indices:
            eco_lifespan[i]=round(perennial.loc[i],4)

        D[currentyear]['eco lifespan']=eco_lifespan

    return D


# ### execution

# In[3]:


global beginyear,endyear
beginyear=2012
endyear=2019


# In[4]:


global eco_coeff,default_discount
eco_coeff=0.7
default_discount=0.8


# In[5]:


prod=pd.read_csv('Production_Crops_E_All_Data_(Normalized).csv',
                 encoding='latin-1')

prix=pd.read_csv('Prices_E_All_Data_(Normalized).csv',
                 encoding='latin-1')

land=pd.read_csv('Inputs_LandUse_E_All_Data_(Normalized).csv',
                 encoding='latin-1')

population=pd.read_csv('Population_E_All_Data_(Normalized).csv',
                      encoding='latin-1')

gdp=pd.read_csv('Macro-Statistics_Key_Indicators_E_All_Data_(Normalized).csv',
                      encoding='latin-1')


# In[6]:


os.chdir('H:/data')


# In[7]:


mapping=pd.read_csv('mapping.csv')


# In[8]:


#select malaysia from beginyear-endyear
malay_land=land[land['Year'].isin(range(beginyear,endyear))][land['Area']=='Malaysia'][land['Element'].isin(['Area'])][land['Item'].isin(['Cropland'])]

malay_prix=prix[prix['Year'].isin(range(beginyear,endyear))][prix['Area']=='Malaysia'][prix['Element']=='Producer Price (USD/tonne)'][prix['Months']=='Annual value']

malay_prod=prod[prod['Year'].isin(range(beginyear,endyear))][prod['Area']=='Malaysia'][prod['Element'].isin(['Area harvested','Production'])]

malay_pop=population[population['Element']=='Total Population - Both sexes'][population['Area']=='Malaysia'][population['Year']>=beginyear]

malay_gdp=gdp[gdp['Element']=='Value US$'][gdp['Item']=='Gross Domestic Product per capita'][gdp['Area']=='Malaysia'][gdp['Year'].isin(range(beginyear,endyear))]


# In[9]:


#exclude land usage<1%
exclude=[813,236,809,1717,
         512, 782, 656, 149, 667, 809,
         813, 689, 698, 702, 723, 217,
         226, 236, 242,463, 603, 619,
         1720, 1729, 1731, 1732, 1735,
         1738, 1753, 1804, 1841,1814]


# In[10]:


#find items without price
a=set(malay_prod['Item Code'][malay_prod['Element']=='Area harvested'])

b=set(malay_prod['Item Code'][malay_prod['Element']=='Production'])

c=set(malay_prix['Item Code'])

sans_prix=[i for i in a.intersection(b) if i not in c]

sans_prix=[i for i in sans_prix if i not in exclude]

print(sans_prix)


# In[11]:


#use austria oilseeds to replace
oilseeds_prix=prix[prix['Area']=='Austria'][prix['Element']=='Producer Price (USD/tonne)'][prix['Item Code']==339][prix['Year'].isin(range(beginyear,endyear))]


# In[12]:


#use avg of maize and rice to replace cereals
cereal_mean=malay_prix[malay_prix['Item'].isin(['Maize','Rice, paddy'])].groupby('Year').mean()['Value'].tolist()

cereal_prix=oilseeds_prix.copy()

cereal_prix['Value']=cereal_mean

cereal_prix['Item']='Cereals (Rice Milled Eqv)'

cereal_prix['Item Code']=1817


# In[13]:


#add missing
malay_prix=malay_prix.append(oilseeds_prix).append(cereal_prix)

malay_prix.reset_index(inplace=True,drop=True)


# In[14]:


#concat
malay_prod=malay_prod.merge(mapping,on=['Item Code', 'Item'],how='left')


# In[15]:


#find inner join of crops
a=set(malay_prod['Item Code'][malay_prod['Element']=='Area harvested'])

b=set(malay_prod['Item Code'][malay_prod['Element']=='Production'])

c=set(malay_prix['Item Code'])

target_crops=a.intersection(b).intersection(c)

targets=[i for i in target_crops if i not in exclude]


# In[16]:


#select crops
malay_prod=malay_prod[malay_prod['Item Code'].isin(targets)]
malay_prix=malay_prix[malay_prix['Item Code'].isin(targets)]


# In[17]:


#add 2018 land
land_2018=malay_land.iloc[-1:].copy()
land_2018.reset_index(inplace=True,drop=True)
land_2018.at[0,'Year']=2018
land_2018.at[0,'Year Code']=2018

malay_land=malay_land.append(land_2018)


# In[18]:


#export to csv
malay_land.to_csv('malay_land.csv',index=False)

malay_prod.to_csv('malay_prod.csv',index=False)

malay_prix.to_csv('malay_prix.csv',index=False)

malay_pop.to_csv('malay_pop.csv',index=False)

malay_gdp.to_csv('malay_gdp.csv',index=False)


# In[19]:


#concat
D=prepare(malay_land,malay_prod,malay_prix)

grand=pd.concat([D[i] for i in D])

grand.reset_index(inplace=True,drop=True)


# In[20]:


#create from synthetic control unit
malay_ginger=[1711.631924118213, 1918.0617150999785, 1926.352662122375, 1904.0526853161766]

malay_lettuce=[808.9104313117714, 809.2907573824596, 880.0718990821069, 801.194381901839]

malay_maize=[176.02653721679235, 181.61446377135653, 185.21444467527138]

malay_orange=[385.20868947337976, 303.6319254759596, 277.51641822220614, 376.92771860265077]

malay_sugarcane=[246.78089608441445]

malay_tobacco=[4345.956117624693,
 4091.368210599639,
 3638.8980233955585,
 3829.529414768218,
 3758.1754705530975,
 3889.6001454970665]


# In[21]:


#fill price
fillnull=dict(zip(grand['Item'][grand['price'].isnull()].unique(),
[malay_tobacco,malay_ginger,malay_lettuce,
 malay_orange,malay_maize,malay_sugarcane,]))

for i in fillnull:
    indices=grand[grand['Item']==i][grand['price'].isnull()].index.tolist()
    for j in indices:
        grand.at[j,'price']=fillnull[i][indices.index(j)]


# In[22]:


grand.to_csv('grand.csv',index=False)


# ### synthetic control unit

# In[23]:


# import statsmodels.api as sm

# #show missing items
# null=set(grand['Item'][grand['price'].isnull()])

# ss=grand[grand['Item'].isin(null)].sort_values(['Item','Year'])

# ss

# #split here

# #create synthetic control unit
# for ii in ss['Item'].unique():
    
#     print(ii)
    
#     #cleanse data
#     temp=prix[prix['Item']==ii][prix['Year'].isin(range(beginyear,endyear))][prix['Element']=='Producer Price (USD/tonne)'][prix['Months']=='Annual value']
#     temp=temp.pivot(index='Year',columns='Area',values='Value')
    
#     #delete null data
#     for i in temp:
#         if temp[i].isnull().any() and i!='Malaysia':
#             del temp[i]
    
#     #train
#     x=temp.loc[temp['Malaysia'].dropna().index]
#     del x['Malaysia']
#     y=temp['Malaysia'].dropna()
#     x.reset_index(inplace=True,drop=True)
#     y.reset_index(inplace=True,drop=True)

#     m=sm.OLS(y,x).fit()
    
#     #train result
#     print(m.predict(),y.tolist())
    
#     #test result
#     test=temp[temp['Malaysia'].isnull()]
#     test=test[[i for i in test.columns if i!='Malaysia']]
#     print(m.predict(test).tolist())

