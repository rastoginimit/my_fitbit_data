from scripts.authenticator import *
import pandas as pd 
import datetime
import sys

client_id      = input("Provide the Client ID: ")
client_secret  = input("Provide the Client Secret: ")

start_date     = input("Enter start date in format YYYY-MM-DD from which the data is to be extracted : ")
end_date       = input("Enter end date in format YYYY-MM-DD up to which the data is to be extracted : ")

fbClient       = FitbitClient(client_id, client_secret)
auth2client    = fbClient.getAuth2Client()

start_date     = fbClient.validateDate(start_date)
end_date       = fbClient.validateDate(end_date)

df_list = list()

days_count = (end_date - start_date).days + 1

for date in (start_date + pd.DateOffset(n) for n in range(days_count)):
    day_data       = auth2client.intraday_time_series('activities/heart', date, detail_level='1sec')
    heartRateZones = day_data['activities-heart'][0]['value']['heartRateZones']
    for hrZone in heartRateZones:
        hrZone["minutes"]=hrZone.get("minutes", 0)
    
    restingHrtRate = day_data['activities-heart'][0]['value'].get('restingHeartRate', 0)
    df             = pd.DataFrame(heartRateZones)
    df['date']     = date.strftime('%Y-%m-%d')
    df['restingHrtRate'] = restingHrtRate
    df_list.append(df)
heart_rate_data = pd.concat(df_list)
heart_rate_data.to_csv("output/heart_rate.csv", index=False)

sleep_fields     = ['dateOfSleep', 'efficiency', 'minutesAwake', 'minutesAfterWakeup', 'minutesAsleep', 'minutesToFallAsleep', 'restlessDuration', 'awakeDuration']
sleep_data       = auth2client.time_series('sleep', base_date=start_date, end_date=end_date)
sleep_list       = sleep_data['sleep']
sleep = list()
for i in range(len(sleep_list)):
    sleep.append({key: value for key, value in sleep_list[i].items() if key in (sleep_fields)})
sleep_df         = pd.DataFrame(sleep)
sleep_df.to_csv('output/sleep.csv', index=False)
