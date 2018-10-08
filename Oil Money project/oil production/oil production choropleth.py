
# coding: utf-8

# In[1]:


import folium
import os
os.chdir('h:/')
import pandas as pd


# In[2]:


#this table comes from wikipedia
# https://en.wikipedia.org/wiki/List_of_countries_by_oil_production
#but i have changed the names of some countries
#try to keep names consistent with geojson file
df=pd.read_csv('oil production choropleth.csv')


# In[3]:


df['Oil Production']=df['Oil Production'].apply(lambda x: x/1000)


# In[4]:


#location takes two arguments, latitude and longitude
#zoom_start implies zoom level
#1 is world map, 2 is continent map, 3 is region map
#4 is country map, 5 is county map etc
m=folium.Map(location=(30,50), zoom_start=4)

#geo_data is a geojson file
#its a file that indicates country shape on a map
#we can download country and even more detailed level from the first link
#the second link converts all the files in first link to geojson
#https://gadm.org/download_country_v3.html
#https://mapshaper.org/
#here i found the map shape from github
#i just cannot find the original link
#so i just upload it to the repo

#data is the dataframe
#columns would be the columns we use in that dataframe
#we need one column for the region name and the other one for value
#the region name should be consistent with the region name in geojson
#and key_on denotes the key in geojson for region names
#fill_color is just matplotlib cmap
#fill_opacity,line_opacity are plotting options
#legend_name is just the name of the label in matplotlib
#threshold_scale can only take up to six values in a list
#for simplicity, we can use from branca.utilities import split_six
#to get the quantile data equally divided into six parts
m.choropleth(
 geo_data=(open("worldmapshape.json",encoding = "utf_8_sig").read()),
 name='choropleth',
 data=df,
 columns=['Country', 'Oil Production'],
 key_on='properties.name',
 fill_color='YlOrRd',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Oil Production Thousand Barrels/Day',
 threshold_scale=[0.0,1.0, 150.0, 800.0, 2000.0, 4000.0]
)

#layout control is just a map filter
#we can unselect choropleth any time
folium.LayerControl().add_to(m)
display(m)

#in general, folium is a really good wrap up for leaflet.js
#it saves me a lot of time from learning javascript
#it is very straight forward, a very flat learning curve
#there is only one thing i hate about it
#which is the location name is always in local language
#at least google map provides english plus local language
#this is quite annoying, other than that, its pretty cool
