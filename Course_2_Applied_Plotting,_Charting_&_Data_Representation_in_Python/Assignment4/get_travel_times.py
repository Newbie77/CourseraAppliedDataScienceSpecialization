import json
import pandas as pd
import requests
import urllib.request
import urllib.parse
import time
from datetime import datetime, timedelta,date

Now = datetime.now()
main_from_date='01.01.2016'
from_time='17:00:00'
to_time='22:00:00'
from_stop='North Station'
to_stop='Waltham'
NumberOfDays = int((Now - datetime.strptime(main_from_date, "%d.%m.%Y")).days)


traveltime= pd.DataFrame(columns=['RouteID','FromStop','ToStop','Departure','Arrival','TravelTimeMin'])
for single_date in (datetime.strptime(main_from_date, "%d.%m.%Y") + timedelta(n) for n in range(NumberOfDays)):
    from_date_time = datetime.strptime(str(str(single_date.strftime("%d.%m.%Y"))+' '+from_time), "%d.%m.%Y %H:%M:%S")
    to_date_time = datetime.strptime(str(str(single_date.strftime("%d.%m.%Y"))+' '+to_time), "%d.%m.%Y %H:%M:%S")


    pattern = '%d.%m.%Y %H:%M:%S'
    from_date_time_epoch =int(from_date_time.timestamp())
    to_date_time_epoch =int(to_date_time.timestamp())
    print(single_date,from_date_time_epoch,to_date_time_epoch)


    params = urllib.parse.urlencode( {
        "api_key": 'wX9NwuHnZU2ToO7GmGR9uw', #public api_key
        "format": 'json',
        "from_stop": from_stop,
        "to_stop":  to_stop,
        "from_datetime":from_date_time_epoch,
        "to_datetime":to_date_time_epoch
        })

    url='http://realtime.mbta.com/developer/api/v2.1/traveltimes?%s' % params

    with urllib.request.urlopen(url) as f:
        data=f.read().decode('utf-8')


    js= json.loads(data)
#print(json.dumps(js, indent=2))

    for i in range(len(js['travel_times'])):
        #print(js['travel_times'][i]['route_id'])

        traveltime.loc[len(traveltime)] = ([
                        js['travel_times'][i]['route_id'],
                        from_stop,
                        to_stop,
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(js['travel_times'][i]['dep_dt']))),
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(js['travel_times'][i]['arr_dt']))),
                        float(js['travel_times'][i]['travel_time_sec'])/60,

                        ])
print(traveltime)
traveltime.to_csv('MBTA/traveltime_cr_all.csv')
