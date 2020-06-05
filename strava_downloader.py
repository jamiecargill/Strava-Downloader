import os
import dotenv
import json
import time
from stravaio import strava_oauth2, StravaIO

def everything_else(token, date = None):
    client = StravaIO(access_token=token['access_token'])

    if date == None:
        activities = client.get_logged_in_athlete_activities()
    else:
        activities = client.get_logged_in_athlete_activities(after=date)

    activity_dict = {}

    for activity in activities:
        activity = activity.to_dict()
        activity_dict[activity["id"]] = activity
    
    activity_json = json.dumps(activity_dict, indent=4, sort_keys=True, default=str)

    file_activities = open("activities.json", "w")
    file_activities.write(activity_json)
    file_activities.close()


def get_token():
    file_token = open("token.json", "r")
    file_contents = file_token.read()
    token = json.loads(file_contents)
    file_token.close()

    currentime = int(time.time())

    if currentime > token["expires_at"]:
        token = get_new_token()
        if token ==  "Client ID or Client Secret Not Present":
            print("Both STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET need to be present in .env")
            return
        else:
            file_token = open("token.json", "w")
            file_token.write(token)
            file_token.close()
    
    return token


def get_new_token():
    STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

    if STRAVA_CLIENT_ID == None or STRAVA_CLIENT_SECRET == None:
        return "Client ID or Client Secret Not Present"

    token = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    token = json.dumps(token)

    return token


def main():
    dotenv.load_dotenv()
    token = get_token()

    if token is not None:
        everything_else(token, "2020-05-31")
        return


if __name__ == "__main__":
    main()