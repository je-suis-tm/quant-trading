
# coding: utf-8

# In[1]:


target_country=['Australia','Spain',
 'Morocco',
 'United Kingdom',
 'Poland',
 'France',
 'Mexico',
 'Bangladesh',
 'Canada',
 'Viet Nam',
 'Thailand',
 'Guatemala',
 'Colombia',
 'Germany',
 'China',
 'Brazil',
 'India',
 'United States of America',
 'Malaysia',
 'Indonesia']


# In[2]:


target_year=[2000,
 2001,
 2002,
 2003,
 2004,
 2005,
 2006,
 2007,
 2008,
 2009,
 2010,
 2011,
 2012,
 2013,
 2014,
 2015,
 2016,
 2017]


# In[3]:


import pandas as pd
import numpy as np
import os
os.chdir('H:/')


# In[4]:


prod=pd.read_csv('Production_Crops_E_All_Data_(Normalized).csv',encoding='latin-1')


# In[5]:


prix=pd.read_csv('Prices_E_All_Data_(Normalized).csv',encoding='latin-1')


# In[6]:


echanger=pd.read_csv('Trade_Crops_Livestock_E_All_Data_(Normalized).csv',encoding='latin-1')


# In[7]:


#only compare crops with available data
target_crops=set(prod['Item']).intersection(set(prix['Item'])).intersection(set(echanger['Item']))


# # volume

# In[8]:


#extract export volume
trade=echanger[echanger['Element']=='Export Quantity']


# In[9]:


#cleanse
trade=trade[trade['Item'].isin(target_crops)]

trade=trade[trade['Area'].isin(target_country)]

trade=trade[trade['Year'].isin(target_year)]

trade=trade[['Area','Year','Item','Value']]


# In[10]:


#extract production data
prod=prod[prod['Element']=='Production']


# In[11]:


#cleanse
prod=prod[prod['Item'].isin(target_crops)]

prod=prod[prod['Area'].isin(target_country)]

prod=prod[prod['Year'].isin(target_year)]

prod=prod[['Area','Year','Item','Value']]


# In[12]:


#group by sum
export=trade.groupby(['Area','Year']).sum()


# In[13]:


#group by sum
supply=prod.groupby(['Area','Year']).sum()


# In[14]:


#create new dataframe to compute export volume percentage
pourcent=pd.DataFrame(index=export.index)


# In[15]:


#compute percentage
pourcent['value']=np.divide(export['Value'].tolist(),supply['Value'].tolist())


# In[16]:


#clean up index
pourcent.reset_index(inplace=True)


# In[17]:


#historical average
mean_pourcent=pourcent[['Area','value']].groupby('Area').mean()


# In[18]:


#sort by percentage
mean_pourcent=mean_pourcent.sort_values('value')


# In[19]:


#export percentage for a particular year
pourcent[pourcent['Year'].isin([2017])].sort_values('value')


# # price

# In[20]:


#get usd price
prix=prix[prix['Element']=='Producer Price (USD/tonne)']


# In[21]:


#cleanse
prix=prix[prix['Item'].isin(target_crops)]

prix=prix[prix['Area'].isin(target_country)]

prix=prix[prix['Year'].isin(target_year)]

prix=prix[['Area','Year','Item','Value']]


# In[22]:


#previously we examine the volume
#now we focus on value
value=prod.merge(prix,on=['Area','Year','Item'],how='inner')


# In[23]:


#volume times unit price equals to total value
value['Value']=np.multiply(value['Value_x'],value['Value_y'])


# In[24]:


#cleanse
value=value[['Area','Year','Item','Value']]


# In[25]:


#get export price
exchange=echanger[echanger['Element']=='Export Value']


# In[26]:


#cleanse
exchange=exchange[exchange['Item'].isin(target_crops)]

exchange=exchange[exchange['Area'].isin(target_country)]

exchange=exchange[exchange['Year'].isin(target_year)]

exchange=exchange[['Area','Year','Item','Value']]


# In[27]:


#group by sum
temp1=exchange.groupby(['Area','Year']).sum()


# In[28]:


#group by sum
temp2=value.groupby(['Area','Year']).sum()


# In[29]:


#inner join
temp=temp1.merge(temp2,on=['Area','Year'],how='inner')


# In[30]:


#create dataframe to compute export value percentage
percentage=pd.DataFrame(index=temp.index)


# In[31]:


#compute export value percentage
percentage['value']=np.divide(temp['Value_x'],temp['Value_y'])


# In[32]:


#clean up
percentage.reset_index(inplace=True)


# In[33]:


#historical average
mean_percentage=percentage[['Area','value']].groupby('Area').mean()


# In[34]:


#sort by percentage
mean_percentage=mean_percentage.sort_values('value')


# In[35]:


#export percentage for a particular year
percentage[percentage['Year'].isin([2016])].sort_values('value')

