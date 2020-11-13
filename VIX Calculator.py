
# coding: utf-8

# In[1]:


#check cboe white paper on the details of computation
# http://www.cboe.com/micro/vix/vixwhite.pdf
#check this awesome article on the connection between vix and variance swap
# https://berentlunde.netlify.app/post/the-fear-index-vix-and-variance-swaps
#check this paper on the variance swap
# https://www.researchgate.net/publication/246869706_More_Than_You_Ever_Wanted_to_Know_About_Volatility_Swaps
import pandas as pd
import datetime as dt
import dateutil
import decimal
import os
import numpy as np
os.chdir('K:/ecole/github/televerser/données')


# In[2]:


#fill weekend and holiday missing cmt rate
def cmt_rate_fill_date(cmt_rate):

    #get missing date as well
    complete_date=pd.date_range(cmt_rate['Date'].min(),cmt_rate['Date'].max())

    #reindex to fill missing date
    cmt_rate=cmt_rate.pivot(index='Date',columns='maturity',values='value')
    cmt_rate=cmt_rate.reindex(complete_date)

    #cleanse
    cmt_rate.index.name='Date'
    cmt_rate.reset_index(inplace=True)

    #ffill
    cmt_rate.fillna(method='ffill',inplace=True)

    #revert to the original form
    cmt_rate=cmt_rate.melt(id_vars='Date',value_vars=['1 Mo', '1 Yr', '10 Yr', '2 Mo', '2 Yr', '20 Yr', '3 Mo',
           '3 Yr', '30 Yr', '5 Yr', '6 Mo', '7 Yr'])
    
    return cmt_rate


# In[3]:


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
        if (dt.datetime.weekday(settlement_day) in range(5)) and \
        (str(settlement_day)[:10] not in public_holidays) and \
        counter>expiration_day-1:
            correct=True
        else:
            settlement_day-=dt.timedelta(days=1)
            
            #weekday is counted even if its federal holiday
            if (dt.datetime.weekday(settlement_day) in range(5)):
                counter+=1
        
    return settlement_day


# In[4]:


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


# In[5]:


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


# In[6]:


#select out of money call options
#with zero prior settle exclusion
def get_options_call_inclusion(options,strike):

    options_call=options[options['options-optiontype']=='call']

    #select outta money options
    #cuz they are usually more liquid
    options_call_otm=options_call[options_call['options-strikePrice']>strike]

    #sort by strike price
    options_call_otm=options_call_otm.sort_values('options-strikePrice')
    options_call_otm.reset_index(inplace=True,drop=True)

    #find all zero prior settle options
    options_call_otm_zeros=options_call_otm[options_call_otm['options-priorSettle']==0]
    options_call_otm_zeros.reset_index(inplace=True)

    #as we dont have bid and ask
    #we use prior settle instead
    #once options with consecutive strike prices have zero prior settle
    #any further out of money options would be excluded
    if options_call_otm_zeros[options_call_otm_zeros['index'].diff()==1].empty:
        ind=len(options_call_otm)
    else:
        ind=options_call_otm_zeros['index'][options_call_otm_zeros['index'].diff()==1].iloc[0]

    #exclude all zero prior settle options
    options_call_inclusion=options_call_otm[options_call_otm['options-priorSettle']!=0][:ind]

    #cleanse
    options_call_inclusion.reset_index(inplace=True,drop=True)
    
    return options_call_inclusion


# In[7]:


#select out of money put options
#with zero prior settle exclusion
def get_options_put_inclusion(options,strike):

    options_put=options[options['options-optiontype']=='put']

    #select outta money options
    #cuz they are usually more liquid
    options_put_otm=options_put[options_put['options-strikePrice']<strike]

    #sort by strike price
    options_put_otm=options_put_otm.sort_values('options-strikePrice',
                                                ascending=False)
    options_put_otm.reset_index(inplace=True,drop=True)

    #find all zero prior settle options
    options_put_otm_zeros=options_put_otm[options_put_otm['options-priorSettle']==0]
    options_put_otm_zeros.reset_index(inplace=True)

    #as we dont have bid and ask
    #we use prior settle instead
    #once options with consecutive strike prices have zero prior settle
    #any further out of money options would be excluded
    if options_put_otm_zeros[options_put_otm_zeros['index'].diff()==1].empty:
        ind=len(options_put_otm)
    else:
        ind=options_put_otm_zeros['index'][options_put_otm_zeros['index'].diff()==1].iloc[0]

    #exclude all zero prior settle options
    options_put_inclusion=options_put_otm[options_put_otm['options-priorSettle']!=0][:ind]

    #cleanse
    options_put_inclusion.reset_index(inplace=True,drop=True)
    
    return options_put_inclusion


# In[8]:


#compute sigma based upon variance swap formula
def compute_sigma(forward,strike,
                  options_call_inclusion,
                  options_put_inclusion,
                  interest_rate,time_to_expiration):

    contributions=0.0
    for i in [options_call_inclusion,
              options_put_inclusion]:
        for j in i.index:
            
            #interval between strike prices
            if j-1<0:
                delta=abs(i['options-strikePrice'][j]-i['options-strikePrice'][j+1])
            elif j+1==len(i):
                delta=abs(i['options-strikePrice'][j]-i['options-strikePrice'][j-1])
            else:
                delta=abs(i['options-strikePrice'][j-1]-i['options-strikePrice'][j+1])/2

            contributions+=i['options-priorSettle'][j]*np.exp(interest_rate*time_to_expiration)*delta/(i['options-strikePrice'][j])**2

    #replace bid ask spread midpoint with prior settle
    sigma=contributions*2/time_to_expiration-((forward/strike-1)**2)/time_to_expiration
    
    return sigma


# In[9]:


#weighted avg of vix
def compute_vix(time_to_expiration_front,
                time_to_expiration_rear,
                sigma_front,sigma_rear,
                num_of_mins_timeframe,
                num_of_mins_year):

    sum1=time_to_expiration_front*sigma_front*(time_to_expiration_rear*num_of_mins_year-num_of_mins_timeframe)/(time_to_expiration_rear*num_of_mins_year-time_to_expiration_front*num_of_mins_year)
    sum2=time_to_expiration_rear*sigma_rear*(num_of_mins_timeframe-time_to_expiration_front*num_of_mins_year)/(time_to_expiration_rear*num_of_mins_year-time_to_expiration_front*num_of_mins_year)
    vix=((sum1+sum2)*num_of_mins_year/num_of_mins_timeframe)**0.5*100
    
    return vix


# In[10]:


#aggregate all functions into one
def vix_calculator(df,cmt_rate,calendar,
                   options_id,tradedate,
                   timeframe_front,timeframe_rear,
                   expiration_hour,expiration_day,
                   num_of_mins_timeframe,num_of_mins_year):
    
    #us federal holidays
    federal_holidays=calendar['DATE'].tolist()
    
    #daily treasury yield curve rate
    interest_rate_front=cmt_rate['value'][cmt_rate['maturity']==f'{timeframe_front} Mo'][cmt_rate['Date']==tradedate].item()/100
    interest_rate_rear=cmt_rate['value'][cmt_rate['maturity']==f'{timeframe_rear} Mo'][cmt_rate['Date']==tradedate].item()/100

    #find current options
    currentoptions=df[df['options-id']==options_id][df['tradeDate']==tradedate].copy()

    #determine next term and near term contracts
    nextterm=dt.datetime.strptime(tradedate,'%Y-%m-%d')+dt.timedelta(days=30*timeframe_rear)
    nearterm=dt.datetime.strptime(tradedate,'%Y-%m-%d')+dt.timedelta(days=30*timeframe_front)

    #determine rear month and front month
    rearmonth=pd.to_datetime(f'{nextterm.year}-{nextterm.month}-1')
    frontmonth=pd.to_datetime(f'{nearterm.year}-{nearterm.month}-1')

    #create dataframe copies
    options_rear=currentoptions[currentoptions['futures-expirationDate']==rearmonth].copy()
    options_front=currentoptions[currentoptions['futures-expirationDate']==frontmonth].copy()

    #take futures updated datetime as the current one
    current_day_front=options_front['futures-updated'].iloc[0]
    current_day_rear=options_rear['futures-updated'].iloc[0]

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

    #get forward level and strike price no larger than forward
    forward_front,strike_front=get_forward_strike(options_front,
                                                  interest_rate_front,
                                                  time_to_expiration_front)

    forward_rear,strike_rear=get_forward_strike(options_rear,
                                                  interest_rate_rear,
                                                  time_to_expiration_rear)

    #prepare options for calculation
    options_call_front_inclusion=get_options_call_inclusion(
        options_front,strike_front)

    options_call_rear_inclusion=get_options_call_inclusion(
        options_rear,strike_rear)

    options_put_front_inclusion=get_options_put_inclusion(
        options_front,strike_front)

    options_put_rear_inclusion=get_options_put_inclusion(
        options_rear,strike_rear)

    #use put call avg 
    #if strike price exists in the out of money dataset
    for i in [options_call_front_inclusion,
              options_put_front_inclusion]:
        if strike_front in i['options-strikePrice'].tolist():
            i['opt'][i['options-strikePrice']==strike_front]=options_front['options-priorSettle'][options_front['options-strikePrice']==strike_front].mean()

    for i in [options_call_rear_inclusion,
              options_put_rear_inclusion]:
        if strike_rear in i['options-strikePrice'].tolist():
            i['opt'][i['options-strikePrice']==strike_rear]=options_rear['options-priorSettle'][options_rear['options-strikePrice']==strike_rear].mean()


    #compute sigmas
    sigma_front=compute_sigma(forward_front,strike_front,
                      options_call_front_inclusion,
                      options_put_front_inclusion,
                      interest_rate_front,time_to_expiration_front)

    sigma_rear=compute_sigma(forward_rear,strike_rear,
                      options_call_rear_inclusion,
                      options_put_rear_inclusion,
                      interest_rate_rear,time_to_expiration_rear)

    #enfin,vix!!!
    vix=compute_vix(time_to_expiration_front,
                    time_to_expiration_rear,
                    sigma_front,sigma_rear,
                    num_of_mins_timeframe,
                    num_of_mins_year)
    
    return vix


# In[11]:


#compute 3 month ahead vix for henry hub european options
def main():

    #read data
    df=pd.read_csv('henry hub european options.csv')
    calendar=pd.read_csv('cme holidays.csv')
    cmt_rate=pd.read_csv('treasury yield curve rates.csv')

    #datetime format
    df['futures-expirationDate']=pd.to_datetime(df['futures-expirationDate'])
    df['tradeDate']=pd.to_datetime(df['tradeDate'])
    df['futures-updated']=pd.to_datetime(df['futures-updated'])
    df['options-updated']=pd.to_datetime(df['options-updated'])
    cmt_rate['Date']=pd.to_datetime(cmt_rate['Date'])

    #fill weekend and holiday missing cmt rate
    cmt_rate=cmt_rate_fill_date(cmt_rate)

    #preset parameters
    #check contractSpecs of the underlying asset
    #in our case
    # https://www.cmegroup.com/trading/energy/natural-gas/natural-gas_contractSpecs_options.html#optionProductId=1352
    options_id=1352;tradedate='2020-11-12'
    timeframe_front=2;timeframe_rear=3
    expiration_hour=16;expiration_day=4
    num_of_mins_timeframe=timeframe_rear*30*24*60
    num_of_mins_year=365*24*60

    #vix!!!
    vix=vix_calculator(df,cmt_rate,calendar,
                       options_id,tradedate,
                       timeframe_front,timeframe_rear,
                       expiration_hour,expiration_day,
                       num_of_mins_timeframe,num_of_mins_year)

    print(vix)


# In[12]:


if __name__ == '__main__':
    main()

