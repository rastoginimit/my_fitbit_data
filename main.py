from scripts.authenticator import *
import pandas as pd 
import datetime
import sys

client_id      = input("Provide the Client ID: ")
client_secret  = input("Provide the Client Secret: ")

date           = input("Enter a date in format YYYY-MM-DD for which the data is to be extacted : ")

fbClient       = FitbitClient(client_id, client_secret)
auth2client    = fbClient.getAuth2Client()

date           = fbClient.validateDate(date)

data           = auth2client.intraday_time_series('activities/heart', date, detail_level='1sec')
heartRateZones = data['activities-heart'][0]['value']['heartRateZones']
restingHrtRate = data['activities-heart'][0]['value']['restingHeartRate']
df             = pd.DataFrame(heartRateZones)
df['date']     = date.strftime('%Y-%m-%d')
df['restingHrtRate'] = restingHrtRate

print(df.head())