import os
import dotenv
import re
import json
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
    file_token = open("token.json", "r")
    file_contents = file_token.read()
    token = json.loads(file_contents)
    file_token.close()

    currentime = int(time.time())

    if currentime > token["expires_at"]:
        token = get_new_token()
        file_token = open("token.json", "w")
        file_token.write(token)
        file_token.close()
    
    return token


def get_new_token():
    STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

    token = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    token = json.dumps(token)

    return token


def set_dotenv(variable, value):
    file_dotenv = open(".env", "r")
    envvars = file_dotenv.readlines()
    file_dotenv.close()

    match = None

    for var in envvars:
        if re.search(variable + "*", var):
            match = var
    
    if match:
        envvars.remove(match)

    envvars.append(variable + '="' + value + '"\n')

    file_dotenv = open(".env", "w")
    file_dotenv.writelines(envvars)
    file_dotenv.close()


def check_dotenv(variable):
    file_dotenv = open(".env", "r")
    envvars = file_dotenv.readlines()
    file_dotenv.close()

    for var in envvars:
        if re.search(variable + "*", var):
            return True

    return False


def setup_dotenv():
    # If .env does not exist, create it
    if not os.path.exists(".env"):
        file_dotenv = open(".env", "w")
        file_dotenv.close()

    # If client ID does not exist, set it
    if not check_dotenv("STRAVA_CLIENT_ID"):
        print('Enter your Strava Client ID:')
        client_id = input()
        set_dotenv("STRAVA_CLIENT_ID", client_id)

    # If client secret does not exist, set it
    if not check_dotenv("STRAVA_CLIENT_SECRET"):
        print('Enter your Strava Client Secret:')
        client_secret = input()
        set_dotenv("STRAVA_CLIENT_SECRET", client_secret)


def main():
    setup_dotenv()
    dotenv.load_dotenv()
    #token = get_token()
    #client = StravaIO(access_token=token['access_token'])
    #get_most_recent_local_activity()

    #if token is not None:
    #    everything_else(client, "2020-05-31")
    #    return


if __name__ == "__main__":
    main()