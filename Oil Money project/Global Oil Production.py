
# coding: utf-8

# In[1]:

#isntalling basemap is pretty painful for anaconda
#try conda install -c conda-forge basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
os.chdir('d:/')


# In[2]:

#need data with value and coordinates to plot
df=pd.read_csv('global oil production.csv')


# In[3]:


ax=plt.figure(figsize=(50,20)).add_subplot(111)

#draw up a world map
#fill continents and country boundaries
m = Basemap()
m.drawmapboundary(fill_color='white', linewidth=0)
m.fillcontinents(color='#c0c0c0',alpha=0.5, lake_color='white')
m.drawcountries(linewidth=1,color='#a79c93')

size=df['oil production']/max(df['oil production'])*20000

#this is crucial if we use a different map projection
x,y=m(df['longitude'].tolist(),df['latitude'].tolist())

m.scatter(x,y, s=size, linewidths=2, edgecolors="#6c6b74", \           
          alpha=0.8,c=df['oil production'],cmap='autumn_r')

for i in range(len(x)):
    plt.text(x[i],y[i], \              
             '%s '%(df['region'][i]), \             
             horizontalalignment='center', \
            verticalalignment='center', \
             size=25)

cb=plt.colorbar(ticks=[1000000,10000000])
cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=22)
cb.ax.set_ylabel('Oil Production 10 Million Barrels per Day', \                  
                 fontsize=22,rotation=270)
plt.title('Global Oil Production by Countries', fontsize=42)

plt.savefig('a.png')

