
# coding: utf-8

# In[1]:


#installing basemap is pretty painful for anaconda
#try conda install -c conda-forge basemap
#if there is filenotfounderror
#try conda install -c conda-forge proj4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
os.chdir('d:/')


# In[2]:


#need data with value and coordinates to plot
#the iron ore production data of 2015 comes from wikipedia
# https://en.wikipedia.org/wiki/List_of_countries_by_iron_ore_production
#the coordinates of each country's capital come from someone's personal blog
# https://lab.lmnixon.org/4th/worldcapitals.html
#note that the capital doesnt necessarily locate at the centre of a country
#to make the figure look better, i slightly change the coordinates
df=pd.read_csv('iron ore production bubble map.csv')


# In[3]:


ax=plt.figure(figsize=(50,20)).add_subplot(111)

#draw up a world map
#fill continents, lakes and country boundaries
m = Basemap()
m.drawmapboundary(fill_color='white', linewidth=0)
m.fillcontinents(color='#c0c0c0',alpha=0.5, lake_color='white')
m.drawcountries(linewidth=1,color='#a79c93')

size=df['iron ore production']/max(df['iron ore production'])*40000

#this is crucial if we use a different map projection
x,y=m(df['longitude'].tolist(),df['latitude'].tolist())

m.scatter(x,y, s=size, linewidths=2, edgecolors="#6c6b74",           
          alpha=0.8,c=df['iron ore production'],cmap='autumn_r')

for i in range(len(x)):
    plt.text(x[i],y[i],               
             '%s '%(df['region'][i]),              
             horizontalalignment='center', 
            verticalalignment='center', 
             size=25)

cb=plt.colorbar(ticks=[10000,800000])
cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=20)
cb.ax.set_ylabel('Iron Ore Production 1000 Tonnes per Year',fontsize=20,rotation=270)
plt.title('Iron Ore Production by Countries', fontsize=42)

plt.show()

