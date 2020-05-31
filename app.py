import os
import dotenv
import json
import re
import time
from stravaio import strava_oauth2, StravaIO

def everything_else(token):
    client = StravaIO(access_token=token['access_token'])

    #athlete = client.get_logged_in_athlete()

    activities = client.get_logged_in_athlete_activities(after='last week')

    with open('activities.txt', 'w') as f:
        for activity in activities:
            f.write("%s\n" % activity)


def get_token():
    f = open("token.json", "r")
    file_contents = f.read()
    token = json.loads(file_contents)
    f.close()

    currentime = int(time.time())

    if currentime > token["expires_at"]:
        token = get_new_token()
        if token ==  "Client ID or Client Secret Not Present":
            print("Both STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET need to be present in .env")
            return
        else:
            f = open("token.json", "w")
            f.write(token)
            f.close()
    
    return token


def get_new_token():
    STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

    if STRAVA_CLIENT_ID == None or STRAVA_CLIENT_SECRET == None:
        return "Client ID or Client Secret Not Present"

    token = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    token = json.dumps(token)

    return token


def setenv(variable, value):
    with open('.env', 'r') as file:
        envvars = file.readlines()
    
    match = None

    for var in envvars:
        if re.search(variable + "*", var):
            match = var
    
    envvars.remove(match)
    envvars.append(variable + '="' + value + '"\n')

    with open('.env', 'w') as file:
        file.writelines(envvars)


def main():
    dotenv.load_dotenv()
    token = get_token()

    if token is not None:
        print(token)
        #everything_else(token)
        return


if __name__ == "__main__":
    main()