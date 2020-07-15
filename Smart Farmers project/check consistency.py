
# coding: utf-8

# In[1]:


import os
os.chdir('H:/')
import pandas as pd


# In[2]:


prod=pd.read_csv('Production_Crops_E_All_Data_(Normalized).csv',
                 encoding='latin-1')

prix=pd.read_csv('Prices_E_All_Data_(Normalized).csv',
                 encoding='latin-1')

land=pd.read_csv('Inputs_LandUse_E_All_Data_(Normalized).csv',
                 encoding='latin-1')


# In[3]:


global beginyear,endyear
beginyear=2012;
endyear=2019


# In[4]:


mapping=pd.read_csv('mapping.csv')


# In[5]:


#select malaysia from 2012-2018
malay_land=land[land['Year'].isin(range(beginyear,endyear))][land['Area']=='Malaysia'][land['Element'].isin(['Area'])][land['Item'].isin(['Cropland'])]

malay_prod=prod[prod['Year'].isin(range(beginyear,endyear))][prod['Area']=='Malaysia'][prod['Element'].isin(['Area harvested','Production'])]

malay_prod=malay_prod.merge(mapping,on=['Item Code', 'Item'],how='left')


# In[6]:


#remove redundant cols
for i in ['Area Code','Element Code','Year Code',
         'Flag','COMMODITY','Item Code',
          'subclass code','class code',
          'DEFINITIONS, COVERAGE, REMARKS',]:
    del malay_prod[i]


# In[7]:


#select crops with available data
a=set(malay_prod['Item'][malay_prod['Element']=='Area harvested'])

b=set(malay_prod['Item'][malay_prod['Element']=='Production'])

target_crops=a.intersection(b)


# In[8]:


#exclude land usage<1% without price data
exclude=['Areca nuts',
 'Bastfibres, other',
 'Cashew nuts, with shell',
 'Cereals, Total',
 'Chillies and peppers, dry',
 'Citrus Fruit, Total',
 'Cloves',
 'Coarse Grain, Total',
 'Coffee, green',
 'Coir',
 'Fibre Crops Primary',
 'Fruit Primary',
 'Fruit, citrus nes',
 'Fruit, fresh nes',
 'Fruit, tropical fresh nes',
 'Groundnuts, with shell',
 'Manila fibre (abaca)',
 'Nutmeg, mace and cardamoms',
 'Oilcrops',
 'Oilcrops, Cake Equivalent',
 'Oilcrops, Oil Equivalent',
 'Roots and Tubers, Total',
 'Roots and tubers nes',
 'Soybeans',
 'Spices nes',
 'Tea',
 'Treenuts, Total',
 'Vegetables Primary',
 'Vegetables, fresh nes']


# In[9]:


#finalize the target
targets=[i for i in target_crops if i not in exclude]


# In[10]:


#cleanse
malay_crops=malay_prod[malay_prod['Item'].isin(targets)]


# In[11]:


#subtotal
total=malay_prod[malay_prod['class'].isnull()]


# In[12]:


#compare sum of area by crops with sum of area by subclass
sss=total[total['Element']=='Area harvested'].groupby(['Item','Year']).sum()

ttt=malay_crops[malay_crops['Element']=='Area harvested'].groupby(['class','Year']).sum()


# In[13]:


#compare sum of area by crops
malay_crops[malay_crops['Element']=='Area harvested'].groupby(['Year']).sum()


# In[14]:


#with cropland
malay_land

