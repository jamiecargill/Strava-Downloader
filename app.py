import os
import dotenv
import json
from stravaio import strava_oauth2, StravaIO

def everything_else(token):
    client = StravaIO(access_token=token['access_token'])

    #athlete = client.get_logged_in_athlete()

    activities = client.get_logged_in_athlete_activities(after='last week')

    with open('activities.txt', 'w') as f:
        for activity in activities:
            f.write("%s\n" % activity)

def get_token():
    STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
    token = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    return token

def main():
    dotenv.load_dotenv()
    token = get_token()
    print(token)

if __name__ == "__main__":
    main()