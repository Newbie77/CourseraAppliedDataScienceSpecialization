import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mt
from datetime import date
from datetime import datetime
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

#Get travel time data from MBTA public API

mbta= pd.read_csv('MBTA/traveltime_cr_all.csv',usecols = [1,2,3,4,5,6])
mbta['DATE']=pd.to_datetime(mbta['Departure'])
mbta['Month']=mbta['DATE'].dt.month
mbta['Year']=mbta['DATE'].dt.year
mbta['DepartureHour']=mbta['DATE'].dt.hour
mbta['DayOfTheWeek'] = mbta['DATE'].dt.dayofweek
mbta=mbta[(mbta['DepartureHour']!=20)]
mbta=mbta[(mbta['DayOfTheWeek']!=6) & (mbta['DayOfTheWeek']!=5)]
avgtraveltime=( pd.DataFrame(mbta.groupby(['Year','Month'])['TravelTimeMin'].mean()) )


weather= pd.read_csv('MBTA/1615554.csv',usecols = [1,5,9,10,13,14])
weather=weather[weather['NAME']=='BOSTON, MA US']
weather['my_date']=pd.to_datetime(weather['DATE'])
weather['Month']=weather['my_date'].dt.month
weather['Year']=weather['my_date'].dt.year
avgprcp=( pd.DataFrame(weather.groupby(['Year','Month'])['PRCP'].mean()) )



merged_data = pd.merge(avgtraveltime, avgprcp, how='left', on=['Year','Month'])
merged_data.reset_index(inplace=True)
merged_data['Day']=1
merged_data['datem'] = pd.to_datetime(merged_data[['Year','Month','Day']],format='%Y%m')

travel=np.array(merged_data['TravelTimeMin'])
PRCP=np.array(merged_data['PRCP'])
datenp=np.array(merged_data['datem'])



## Plotting
cc=np.corrcoef(travel, PRCP)[0][1]
print('Correlation Coefficient',cc)

fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(111)

ax1.plot(travel, '-',linewidth=2,color='grey', label='Travel Time')
ax1.spines['top'].set_visible(False)
ax1.set_ylabel('Average Travel Time (minutes)', alpha=0.8)

ticklabels = [datetime.date( (merged_data.loc[item,'datem'])).strftime( "%b %y") for item in merged_data.index]
ax1.set_xticks(np.arange(1,40))
ax1.set_xticklabels(ticklabels)

for label in ax1.xaxis.get_ticklabels():
    label.set_visible(False)
plt.locator_params(axis='x')

for label in ax1.xaxis.get_ticklabels()[::2]:
    label.set_visible(True)
plt.locator_params(axis='x')

ax1.tick_params(axis=u'x', which=u'both',length=0)

for item in ax1.xaxis.get_ticklabels():
    item.set_rotation(45)

ax2 = ax1.twinx()
ax2.plot(PRCP, '-',linewidth=2,color='royalblue', label='Precipitation')
ax2.set_ylabel('Average Precipitation (inches)', alpha=0.8)
ax2.spines['top'].set_visible(False)



plt.title("Commuter Rail Travel Time From North Station, Boston to Waltham \n Relative to Precipitation on Weekdays from 5 pm to 8 pm, 2016-2018", loc='center', alpha=0.8,fontsize=12)
ax1.annotate('Correlation Coefficient %s' %round(100*cc,0)+'%',xy=(30, 20), xytext=(0, 23))
fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
ax1.set_ylim(15,24)
ax2.set_ylim(0)
plt.show()
