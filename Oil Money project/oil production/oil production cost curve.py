
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('d:/')
import pandas as pd


# In[2]:


#traditional commodity cost curve
#input two pandas series, the third one is optional
def cost_curve(x,y1,y2=[],
               hline_var=0,hline_color='k',hline_name='',
               colormap='tab20c',legends=[],notes=[],
               ylabel='',xlabel='',title='',fig_size=(10,5)):
    
    ax=plt.figure(figsize=fig_size).add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    #set bar location on x axis
    wid=x
    cumwid=[0]
    for i in range(1,len(wid)):
        cumwid.append(wid[i-1]+cumwid[-1])

    #assign colors to different bars from cmap
    cmap=plt.cm.get_cmap(colormap)
    colors=[cmap(i) for i in np.linspace(0,1,len(y1))]
    colors2=[tuple([i/1.3 for i in j if i!=1]+[1.0]) for j in colors]
    
    for i in range(len(y1)):
        plt.bar(cumwid[i],            
                y1[i],width=wid[i],label=legends[i] if len(legends)>0 else '',
                   color=colors[i],align='edge')
        
        if len(y2)>0:
            plt.bar(cumwid[i],            
                    y2[i],width=wid[i],
                   color=colors2[i],bottom=y1[i],align='edge'
                   )
    
    #plot percentile line if needed
    plt.axhline(y=hline_var, linestyle='--',
                c=hline_color,label=hline_name)

    plt.title(title,pad=20)
    ax.yaxis.labelpad=10
    ax.xaxis.labelpad=10
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    
    #slightly expand x axis to look nicer
    plt.xlim(min(cumwid),max(cumwid)+list(wid)[-1])
    plt.xticks([min(cumwid),
                np.mean([min(cumwid),
                         max(cumwid)+list(wid)[-1]]),
                1.01*max(cumwid)+list(wid)[-1]])
    
    #if cost curve breakdown is provided
    #add legends to the right
    if len(y2)>0:
        plt.text(1.1*max(cumwid)+list(wid)[-1],
             list(y1)[-1]/2,notes[0],
                 verticalalignment='center', horizontalalignment='center')
        plt.text(1.1*max(cumwid)+list(wid)[-1],
             list(y1)[-1]+list(y2)[-1]/2,notes[1],
                verticalalignment='center', horizontalalignment='center')
    
    #legends of cost curve for different entities is plotted below the chart
    plt.legend(loc=6,bbox_to_anchor=(0.12, -0.4), ncol=4)    
    
    plt.show()
    


# In[3]:

#why there is only 2015 data?
#well, they said data is the new oil
#especially true when it comes to oil data

#i can only find oil production cost data of 2015 from the below address
# https://www.statista.com/statistics/597669/cost-breakdown-of-producing-one-barrel-of-oil-in-the-worlds-leading-oil-producing-countries/
#and i have to do some scraping to actually get the data
#if u dont know scraping, that will be a problem
#data scientists cant wait for engineers to feed you data
#maybe its time for you to learn
# https://github.com/je-suis-tm/web-scraping

#also you can use oil breakeven price to replace cost data
#the following two links contain quite a lot of information
#sadly, fiscal breakeven price is widely used by opec countries
#if u have other countries in mind, you will be disappointed
# https://www.cfr.org/report/interactive-oil-exporters-external-breakeven-prices
# http://graphics.wsj.com/oil-barrel-breakdown/

#daily production data and proven reserve comes from bp
# https://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy.html
#production capacity is a typical x axis for cost curve
#you can find them from imf or eia, but again, only for opec countries
#therefore, i used daily production data as alternative
# https://www.imf.org/~/media/Files/Publications/REO/MCD-CCA/2018/May/English/mreo0518-statisticalappendix-elsx.ashx
# https://www.eia.gov/opendata/qb.php?sdid=STEO.COPC_AG.A

df=pd.read_csv('global oil cost curve.csv')


# In[4]:


cost_curve(df['Daily production mil barrels'],
           df['Operational cost dollar per barrel'],
           df['Capital cost dollar per barrel'],
           legends=df['Country'],
           notes=['Operational Cost','Capital Cost'],
           hline_var=np.percentile(df['Total cost dollar per barrel'],90),
           hline_color='#e08314',
           hline_name='90% Percentile',
           xlabel='Daily Production, Million Barrels',
           ylabel='US Dollar per Barrel',
           title='2015 Global Oil Cost Curve')

