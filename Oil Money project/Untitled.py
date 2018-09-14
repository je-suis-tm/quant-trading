
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
os.chdir('d:/')


# In[61]:


df=pd.read_csv('global oil production.csv')


# In[70]:


ax=plt.figure(figsize=(50,20)).add_subplot(111)

m = Basemap()
m.drawmapboundary(fill_color='white', linewidth=0)
m.fillcontinents(color='#c0c0c0',alpha=0.5, lake_color='white')
m.drawcountries(linewidth=1,color='#a79c93')

size=df['oil production']/max(df['oil production'])*20000
x,y=m(df['longitude'].tolist(),df['latitude'].tolist())

m.scatter(x,y, s=size, linewidths=2, edgecolors="#6c6b74",           alpha=0.8,c=df['oil production'],cmap='autumn_r')

for i in range(len(x)):
    plt.text(x[i],y[i],              '%s '%(df['region'][i]),             horizontalalignment='center',
            verticalalignment='center',\
             size=25)

cb=plt.colorbar(ticks=[1000000,10000000])
cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=22)
cb.ax.set_ylabel('Oil Production 10 Million Barrels per Day',                  fontsize=22,rotation=270)
plt.title('Global Oil Production by Countries', fontsize=42)

plt.savefig('a.png')

