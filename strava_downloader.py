import os
import dotenv
import re
import json
import time
from stravaio import strava_oauth2, StravaIO

def write_activities_to_file(activity_json):
    file_activities = open("activities.json", "w")
    file_activities.write(activity_json)
    file_activities.close()


def get_activities(client, date = None):
    if date is None:
        activities = client.get_logged_in_athlete_activities()
    else:
        activities = client.get_logged_in_athlete_activities(after=date)

    activity_dict = {}

    for activity in activities:
        activity = activity.to_dict()
        activity_dict[activity["id"]] = activity
    
    activity_json = json.dumps(activity_dict, indent=4, sort_keys=True, default=str)

    return activity_json


#WIP
def get_most_recent_local_activity():
    file_activities = open("activities.json", "r")
    #file_activities_contents = file_activities.read()
    #activities = json.loads(file_activities_contents)
    file_activities.close()


def get_token():
    # Get locally stored token
    token = get_local_token()

    # If token has expired, get new token
    if int(time.time()) > token["expires_at"]:
        get_new_token()
        token = get_local_token()
    
    return token


def get_local_token():
    # If token.json does not exist, create it
    if not os.path.exists("token.json"):
        file_token = open("token.json", "w")
        file_token.write({"expires_at": 0})
        file_token.close()
    
    file_token = open("token.json", "r")
    file_contents = file_token.read()
    token = json.loads(file_contents)
    file_token.close()
    return token


def get_new_token():
    token = strava_oauth2()
    token = json.dumps(token)

    file_token = open("token.json", "w")
    file_token.write(token)
    file_token.close()

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
    # Check and load .env
    setup_dotenv()
    dotenv.load_dotenv()

    # Get token
    token = get_token()
    client = StravaIO(access_token=token['access_token'])

    # Get all activities and write to file
    activity_json = get_activities(client, "2020-06-06")
    write_activities_to_file(activity_json)


if __name__ == "__main__":
    main()