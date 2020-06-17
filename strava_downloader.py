import os
import dotenv
import re
import json
import datetime
from stravaio import strava_oauth2, StravaIO


def write_activities_to_file(activity_dict):
    # If activities.json exists and is not empty
    if os.path.exists("activities.json") and os.stat("activities.json").st_size != 0:
        # Open file and load contents into dict
        file_activities = open("activities.json", "r")
        file_activities_contents = file_activities.read()
        file_activities.close()
        activities = json.loads(file_activities_contents)

        # For each new activity passed in, append to the existing activity dict IF it doesn't already exist
        for activity in activity_dict:
            if str(activity) not in activities:
                activities[str(activity)] = activity_dict[activity]

        activity_json = json.dumps(activities, indent=4, sort_keys=True, default=str)
    else:
        activity_json = json.dumps(activity_dict, indent=4, sort_keys=True, default=str)

    # Write new json to file and close
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

    return activity_dict


def get_most_recent_local_activity():
    if not os.path.exists("activities.json"):
        return None
    
    file_activities = open("activities.json", "r")
    file_activities_contents = file_activities.read()
    file_activities.close()

    try:
        activities = json.loads(file_activities_contents)
    except json.decoder.JSONDecodeError:
        # File empty
        return None

    last_activity_date = "1970-01-01 00:00:00+00:00"

    for activity in activities.values():
        if activity["start_date"] > last_activity_date:
            last_activity_date = activity["start_date"]
    
    last_activity_date = datetime.datetime.strptime(last_activity_date, '%Y-%m-%d %H:%M:%S%z')

    return last_activity_date


def get_token():
    # Get locally stored token
    token = get_local_token()
    current_time=datetime.datetime.now()

    # If token has expired, get new token
    if int(current_time.timestamp()) > token["expires_at"]:
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

    # Get the last locally-stored activity
    last_activity_date = get_most_recent_local_activity()

    # Get the date seven days prior, in case any activities were uploaded late
    if last_activity_date is None:
        date_to_get = None
    else:
        date_to_get = last_activity_date - datetime.timedelta(days=7)

    # Get all activities and write to file
    activity_dict = get_activities(client, date_to_get)
    write_activities_to_file(activity_dict)


if __name__ == "__main__":
    main()