
# coding: utf-8

# In[1]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import copy
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d
import matplotlib.cm as cm
import statsmodels.api as sm
import numpy as np
from sklearn.cluster import KMeans
os.chdir('d:/')


# In[2]:

def dual_axis_plot(xaxis,data1,data2,fst_color='r',
                    sec_color='b',fig_size=(10,5),
                   x_label='',y_label1='',y_label2='',
                   legend1='',legend2='',grid=False,title=''):
    
    fig=plt.figure(figsize=fig_size)
    ax=fig.add_subplot(111)
    

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label1, color=fst_color)
    ax.plot(xaxis, data1, color=fst_color,label=legend1)
    ax.tick_params(axis='y',labelcolor=fst_color)
    ax.yaxis.labelpad=15

    plt.legend(loc=3)
    ax2=ax.twinx()

    ax2.set_ylabel(y_label2, color=sec_color,rotation=270)
    ax2.plot(xaxis, data2, color=sec_color,label=legend2)
    ax2.tick_params(axis='y',labelcolor=sec_color)
    ax2.yaxis.labelpad=15

    fig.tight_layout()
    plt.legend(loc=4)
    plt.grid(grid)
    plt.title(title)
    plt.show()

def get_distance(x,y,a,b):
    
    temp1=y-x*a-b
    temp2=(a**2+1)**0.5
    
    return np.abs(temp1/temp2)

def get_line_params(x1,y1,x2,y2):
    
    a=(y1-y2)/(x1-x2)
    b=y1-a*x1
    
    return a,b


# In[3]:


df=pd.read_csv('wcs crude cadaud.csv',encoding='utf-8')
df.set_index('date',inplace=True)


# In[4]:


df.index=pd.to_datetime(df.index,format='%m/%d/%Y')


# In[5]:


df=df.reindex(columns=
['cny',
 'gbp',
 'usd',
 'eur',
 'krw',
 'mxn',
 'gas',
 'wcs',
 'edmonton',
 'wti',
 'gold',
 'jpy',
 'cad'])


# In[6]:


var=locals()

for i in df.columns:
    if i!='cad':
            x=sm.add_constant(df[i])
            y=df['cad']
            m=sm.OLS(y,x).fit()
            var[str(i)]=m.rsquared
     
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

width=0.7
colorlist=['#9499a6','#9499a6','#9499a6','#9499a6',
           '#9499a6','#9499a6','#9499a6','#582a20',
           '#be7052','#f2c083','#9499a6','#9499a6']

temp=list(df.columns)
for i in temp:
    if i!='cad':
        plt.bar(temp.index(i)+width,            
            var[str(i)],width=width,label=i,
               color=colorlist[temp.index(i)])
 
plt.title('Regressions on Loonie')
plt.ylabel('R Squared\n')
plt.xlabel('\nRegressors')
plt.xticks(np.arange(len(temp))+width,
           ['Yuan', 'Sterling', 'Dollar', 'Euro', 'KRW',
             'MXN', 'Gas', 'WCS', 'Edmonton',
             'WTI', 'Gold', 'Yen'],fontsize=10)
plt.show()


# In[7]:


ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['cny']/df['cny'].iloc[0]).plot(c='#283670',label='Yuan')
(df['gbp']/df['gbp'].iloc[0]).plot(c='#fe4d32',label='Sterling')
(df['cad']/df['cad'].iloc[0]).plot(c='#484a25',label='Loonie')
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Loonie vs Yuan vs Sterling')
plt.show()


# In[8]:


ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['wti']/df['wti'].iloc[0]).plot(c='#2a78b2',label='WTI',alpha=0.5)
(df['wcs']/df['wcs'].iloc[0]).plot(c='#7b68ee',label='WCS',alpha=0.5)
(df['edmonton']/df['edmonton'].iloc[0]).plot(c='#110b3c',
                                             label='Edmonton',alpha=0.5)
(df['cad']/df['cad'].iloc[0]).plot(c='#cb8b8b',label='Loonie')
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Loonie vs Crude Oil Blends')
plt.show()


# In[9]:


df['date']=[i for i in range(len(df.index))]

x=df[['cad','wcs','date']].reset_index(drop=True)

sse=[]
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(x)
    sse.append(kmeans.inertia_/10000)

a,b=get_line_params(0,sse[0],len(sse)-1,sse[-1])

distance=[]
for i in range(len(sse)):    
    distance.append(get_distance(i,sse[i],a,b))
  
  
# In[10]:


dual_axis_plot([i for i in range(len(distance))],sse,distance,
               x_label='Numbers of Cluster',y_label1='Sum of Squared Error',
               y_label2='Perpendicular Distance',legend1='SSE',legend2='Distance',
               title='Elbow Method for K Means',fst_color='#116466',sec_color='#e85a4f')


# In[11]:


clf=KMeans(n_clusters=2).fit(x)
df['class']=clf.predict(x)
threshold=df[df['class']==0].index[-1]


# In[12]:

ax=plt.figure(figsize=(10,7)).add_subplot(111, projection='3d')


xdata=df['wcs']
ydata=df['cad']
zdata=df['date']
ax.scatter3D(xdata[df['class']==0],ydata[df['class']==0],
             zdata[df['class']==0],c='#faed26',s=10,alpha=0.5,
             label='Before {}'.format(threshold.strftime('%Y-%m-%d')))
ax.scatter3D(xdata[df['class']==1],ydata[df['class']==1],
             zdata[df['class']==1],c='#46344e',s=10,alpha=0.5,
             label='After {}'.format(threshold.strftime('%Y-%m-%d')))
ax.grid(False)
for i in ax.w_xaxis, ax.w_yaxis, ax.w_zaxis:
    i.pane.set_visible(False)  
    
ax.set_xlabel('WCS')
ax.set_ylabel('Loonie')
ax.set_zlabel('Date')
ax.set_title('K Means on Loonie')
ax.legend(loc=6,bbox_to_anchor=(0.12, -0.1), ncol=4)

plt.show()
