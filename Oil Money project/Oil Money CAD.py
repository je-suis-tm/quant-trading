
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
from sklearn.metrics import silhouette_score,silhouette_samples
from sklearn.model_selection import train_test_split
os.chdir('d:/')


# In[2]:

#plot two curves on same x axis, different y axis
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

#get distance between a point and a line
def get_distance(x,y,a,b):
    
    temp1=y-x*a-b
    temp2=(a**2+1)**0.5
    
    return np.abs(temp1/temp2)

#create line equation from two points
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

#create r squared bar charts

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

#normalized value of loonie,yuan and sterling

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['cny']/df['cny'].iloc[0]).plot(c='#77c9d4',label='Yuan')
(df['gbp']/df['gbp'].iloc[0]).plot(c='#57bc90',label='Sterling')
(df['cad']/df['cad'].iloc[0]).plot(c='#015249',label='Loonie')

plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Loonie vs Yuan vs Sterling')
plt.show()


# In[8]:

#normalized value of wti,wcs and edmonton

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

(df['wti']/df['wti'].iloc[0]).plot(c='#2a78b2',
                                   label='WTI',alpha=0.5)
(df['wcs']/df['wcs'].iloc[0]).plot(c='#7b68ee',
                                   label='WCS',alpha=0.5)
(df['edmonton']/df['edmonton'].iloc[0]).plot(c='#110b3c',
                                             label='Edmonton',alpha=0.5)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Normalized Value by 100')
plt.title('Crude Oil Blends')
plt.show()


# In[9]:


dual_axis_plot(df.index,df['cad'],df['wcs'],
               x_label='Date',y_label1='Canadian Dollar',
               y_label2='Western Canadian Select',
               legend1='Loonie',
               legend2='WCS',
               title='Loonie VS WCS in AUD',
               fst_color='#a5a77f',sec_color='#d8dc2c')

dual_axis_plot(df.index,
               np.divide(df['cad'],df['usd']),
               np.divide(df['wcs'],df['usd']),
               x_label='Date',y_label1='Canadian Dollar',
               y_label2='Western Canadian Select',
               legend1='Loonie',
               legend2='WCS',
               title='Loonie VS WCS in USD',
               fst_color='#eb712f',sec_color='#91371b')


# In[10]:

#using elbow method to find optimal number of clusters

df['date']=[i for i in range(len(df.index))]

x=df[['cad','wcs','date']].reset_index(drop=True)

sse=[]
for i in range(1, 8):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(x)
    sse.append(kmeans.inertia_/10000)

a,b=get_line_params(0,sse[0],len(sse)-1,sse[-1])

distance=[]
for i in range(len(sse)):    
    distance.append(get_distance(i,sse[i],a,b))

dual_axis_plot(np.arange(1,len(distance)+1),sse,distance,
               x_label='Numbers of Cluster',y_label1='Sum of Squared Error',
               y_label2='Perpendicular Distance',legend1='SSE',legend2='Distance',
               title='Elbow Method for K Means',fst_color='#116466',sec_color='#e85a4f')
  
  
  
# In[11]:

#using silhouette score to find optimal number of clusters

sil=[]
for n in range(2,8):
    
    clf=KMeans(n).fit(x)
    projection=clf.predict(x)
        
    sil.append(silhouette_score(x,projection))
    
ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.plot(np.arange(2,len(sil)+2),sil,
       label='Silhouette',c='#5c0811',
       drawstyle='steps-mid')
ax.plot(sil.index(max(sil))+2,max(sil),
        marker='*',markersize=20,lw=0,
       label='Max Score',c='#d94330')

plt.ylabel('Silhouette Score')
plt.xlabel('Numbers of Cluster')
plt.title('Silhouette Analysis for K Means')
plt.legend(loc=0)
plt.show()


# In[12]:

#k means

clf=KMeans(n_clusters=2).fit(x)
df['class']=clf.predict(x)
threshold=df[df['class']==0].index[-1]


# In[13]:

#plot clusters in 3d figure

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

#to generate gif, u can use the following code
#it generates 3d figures from different angles
#use imageio to concatenate 
"""
for ii in range(0,360,10):
    ax.view_init(elev=10., azim=ii)
    plt.savefig("cad kmeans%d.png" % (ii))

import imageio

filenames=["movie%d.png" % (ii) for ii in range(0,360,10)] 

images=list(map(lambda filename:imageio.imread(filename),
                filenames))

imageio.mimsave('cad kmeans.gif',images,duration = 0.2)
"""

# In[14]:

#create before/after regression comparison
#the threshold is based upon the finding of k means

m=sm.OLS(df['cad'][df['class']==0],sm.add_constant(df['wcs'][df['class']==0])).fit()
before=m.rsquared
m=sm.OLS(df['cad'][df['class']==1],sm.add_constant(df['wcs'][df['class']==1])).fit()
after=m.rsquared

ax=plt.figure(figsize=(10,5)).add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.bar(['Before {}'.format(threshold.strftime('%Y-%m-%d')),
         'After {}'.format(threshold.strftime('%Y-%m-%d'))],
        [before,after],color=['#f172a1','#a1c3d1'])
plt.ylabel('R Squared')
plt.title('Cluster + Regression')
plt.show()



# In[15]:

#create 1 std, 2 std band

for i in range(2):
    
    x_train,x_test,y_train,y_test=train_test_split(
        sm.add_constant(df['wcs'][df['class']==i]),
        df['cad'][df['class']==i],test_size=0.5,shuffle=False)
    
    m=sm.OLS(y_test,x_test).fit()
    
    forecast=m.predict(x_test)
    
    ax=plt.figure(figsize=(10,5)).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    forecast.plot(label='Fitted',c='#ab987a')
    y_test.plot(label='Actual',c='#ff533d')
    ax.fill_between(y_test.index,
                    forecast+np.std(m.resid),
                    forecast-np.std(m.resid),
                    color='#0f1626', \
                    alpha=0.6, \
                    label='1 Sigma')
    
    ax.fill_between(y_test.index,
                    forecast+2*np.std(m.resid),
                    forecast-2*np.std(m.resid),
                    color='#0f1626', \
                    alpha=0.8, \
                    label='2 Sigma')
    
    plt.legend(loc=0)
    title='Before '+threshold.strftime('%Y-%m-%d') if i==0 else 'After '+threshold.strftime('%Y-%m-%d')
    plt.title(f'{title}\nCanadian Dollar Positions\nR Squared {round(m.rsquared*100,2)}%\n')
    plt.xlabel('\nDate')
    plt.ylabel('CADAUD')
    plt.show()




