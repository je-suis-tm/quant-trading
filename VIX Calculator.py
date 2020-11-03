
# coding: utf-8

# In[1]:


#check cboe white paper on the details of computation
# http://www.cboe.com/micro/vix/vixwhite.pdf
#check this awesome article on the connection between vix and variance swap
# https://berentlunde.netlify.app/post/the-fear-index-vix-and-variance-swaps
import pandas as pd
import datetime as dt
import dateutil
import decimal
import os
import numpy as np
os.chdir('K:/ecole/github/televerser/données')


# In[2]:


#get settlement day in datetime format
#you can scrape the following website of cme instead
# f'https://www.cmegroup.com/CmeWS/mvc/ProductCalendar/Options/{futures_id}?optionTypeFilter=&optionTypeFilter='
#however it has some conflicts with cme globex s own holiday calendar
# https://www.cmegroup.com/tools-information/holiday-calendar.html
def get_settlement_day(current_day,time_horizon,
                       expiration_day,expiration_hour,
                       public_holidays):

    #get month end at expiration hour
    month_end=current_day+dateutil.relativedelta.relativedelta(day=31,hour=expiration_hour,
                                                                    minute=0,second=0,
                                                                   microsecond=0,
                                                                    months=+time_horizon-1)

    
    #adjust to the nth last day of the month
    settlement_day=month_end
    
    #use loop to skip non trading day
    correct=False
    
    #count the month end if its a weekday
    counter=1 if dt.datetime.weekday(settlement_day) in range(5) else 0
    while not correct:
        
        #cannot be a weekend day or a federal holiday
        if (dt.datetime.weekday(settlement_day) in range(5)) and         (str(settlement_day)[:10] not in public_holidays) and         counter>expiration_day-1:
            correct=True
        else:
            settlement_day-=dt.timedelta(days=1)
            
            #weekday is counted even if its federal holiday
            if (dt.datetime.weekday(settlement_day) in range(5)):
                counter+=1
        
    return settlement_day


# In[3]:


#get time to expiration
#instead of current day+settlement day+other days
#we can directly use timedelta to obtain the result in minutes
#no need to skip any holidays in this calculation
def get_time_to_expiration(current_day,time_horizon,
                           expiration_day,expiration_hour,
                           public_holidays):

    #get settlement day
    settlement_day=get_settlement_day(current_day,time_horizon,
                                       expiration_day,expiration_hour,
                                       public_holidays)

    #convert seconds to minutes
    #divided by minutes in a year
    return (settlement_day-current_day).total_seconds()/60/525600


# In[4]:


#get forward level and strike price no larger than forward
def get_forward_strike(options,
                       interest_rate,
                       time_to_expiration):

    #cleanse
    options=options.sort_values('options-strikePrice')
    find_forward=options.pivot(index='options-strikePrice',
                         columns='options-optiontype',
                        values='options-priorSettle')

    #find the forward level with the least put call disparity
    min_diff_ind=(find_forward['call']-find_forward['put']).apply(abs).idxmin()
    min_diff=float(decimal.Decimal(find_forward['call'][min_diff_ind].astype(str))-decimal.Decimal(find_forward['put'][min_diff_ind].astype(str)))
    forward=min_diff_ind+np.e**(interest_rate*time_to_expiration)*(min_diff)

    #find the strike price no larger than forward level
    strike=find_forward.index[find_forward.index<=forward][-1]
    
    return forward,strike


# In[5]:


#read data
df=pd.read_csv('henry hub european options.csv')
calendar=pd.read_csv('cme holidays.csv')
cmt_rate=pd.read_csv('treasury yield curve rates.csv')


# In[6]:


#us federal holidays
federal_holidays=calendar['DATE'].tolist()


# In[7]:


#datetime format
df['futures-expirationDate']=pd.to_datetime(df['futures-expirationDate'])
df['tradeDate']=pd.to_datetime(df['tradeDate'])
df['futures-updated']=pd.to_datetime(df['futures-updated'])
df['options-updated']=pd.to_datetime(df['options-updated'])
cmt_rate['Date']=pd.to_datetime(cmt_rate['Date'])


# In[8]:


#preset parameters
#check contractSpecs of the underlying asset
#in our case
# https://www.cmegroup.com/trading/energy/natural-gas/natural-gas_contractSpecs_options.html#optionProductId=1352
options_id=1352;tradedate='2020-10-15'
timeframe_front=2;timeframe_rear=3
expiration_hour=16;expiration_day=4
interest_rate_front=cmt_rate['value'][cmt_rate['maturity']==f'{timeframe_front} Mo'][cmt_rate['Date']==tradedate].item()/100
interest_rate_rear=cmt_rate['value'][cmt_rate['maturity']==f'{timeframe_rear} Mo'][cmt_rate['Date']==tradedate].item()/100


# In[9]:


currentoptions=df[df['options-id']==options_id][df['tradeDate']==tradedate].copy()


# In[10]:


#determine next term and near term contracts
nextterm=dt.datetime.strptime(tradedate,'%Y-%m-%d')+dt.timedelta(days=30*timeframe_rear)
nearterm=dt.datetime.strptime(tradedate,'%Y-%m-%d')+dt.timedelta(days=30*timeframe_front)


# In[11]:


#determine rear month and front month
rearmonth=pd.to_datetime(f'{nextterm.year}-{nextterm.month}-1')
frontmonth=pd.to_datetime(f'{nearterm.year}-{nearterm.month}-1')


# In[12]:


#create dataframe copies
options_rear=currentoptions[currentoptions['futures-expirationDate']==rearmonth].copy()
options_front=currentoptions[currentoptions['futures-expirationDate']==frontmonth].copy()


# In[13]:


#take futures updated datetime as the current one
current_day_front=options_front['futures-updated'].iloc[0]
current_day_rear=options_rear['futures-updated'].iloc[0]


# In[14]:


#get time to expiration
time_to_expiration_front=get_time_to_expiration(current_day_front,
                                                timeframe_front,
                                                expiration_day,
                                                expiration_hour,
                                                federal_holidays)

time_to_expiration_rear=get_time_to_expiration(current_day_rear,
                                                timeframe_rear,
                                                expiration_day,
                                                expiration_hour,
                                                federal_holidays)


# In[15]:


#get forward level and strike price no larger than forward
forward_front,strike_front=get_forward_strike(options_front,
                                              interest_rate_front,
                                              time_to_expiration_front)

forward_rear,strike_rear=get_forward_strike(options_rear,
                                              interest_rate_rear,
                                              time_to_expiration_rear)

