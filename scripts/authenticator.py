import pandas as pd
from .gather_keys_oauth2 import OAuth2Server
from .fitbit import *

class FitbitClient:
    def __init__(self, client_id, client_secret):
        self.client_id     = client_id
        self.client_secret = client_secret
    def getAuth2Client(self):
        server=OAuth2Server(self.client_id, self.client_secret)
        server.browser_authorize()
        ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
        auth2_client=Fitbit(self.client_id,self.client_secret,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)
        return auth2_client
    def validateDate(self, date):
        dateparts = date.split("-")
        datePartsCount = len(dateparts)
        if(not (datePartsCount==3)):
            print("Invalid date format entered")
            sys.exit()
        year  = dateparts[0]
        month = dateparts[1]
        day   = dateparts[2]

        if (not(year.isnumeric() and len(year)==4 and month.isnumeric() and len(month)==2 and day.isnumeric() and len(day)==2)):
            print("Invalid date format entered")
            sys.exit()
        return pd.datetime(int(year), int(month), int(day))