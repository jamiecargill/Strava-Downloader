# Strava-Downloader

This script downloads all of your Strava activities to a JSON file. Running it again will fetch any recent activities and append them to the file.

The output will contain the standard response from the [Strava API](https://developers.strava.com/docs/reference/#api-Activities-getActivityById) as the value, and the activity ID as the key, like so:

```json
"0123454321": {
    "id": 0123454321,
    "external_id": "2020-06-06-150348-Running-Jamie?s Apple?Watch.fit",
    "upload_id": 0123454321,
    "athlete": {
        "id": 0123456
    },
    "name": "Afternoon Run",
    "distance": 14452.0,
    "moving_time": 4372,
    "elapsed_time": 4759,
    "total_elevation_gain": 72.6,
    "elev_high": 41.6,
    "elev_low": 2.9,
    "type": "Run",
    "start_date": "2020-06-06 14:03:51+00:00",
    "start_date_local": "2020-06-06 15:03:51+00:00",
    "timezone": "(GMT+00:00) Europe/London",
    "start_latlng": [
        0,
        0
    ],
    "end_latlng": [
        0,
        0
    ],
    "achievement_count": 2,
    "kudos_count": 0,
    "comment_count": 0,
    "athlete_count": 1,
    "photo_count": 0,
    "total_photo_count": 0,
    "map": {
        "id": "a0123456789",
        "polyline": null,
        "summary_polyline": "qwertyuiop"
    },
    "trainer": false,
    "commute": false,
    "manual": false,
    "private": false,
    "flagged": false,
    "workout_type": null,
    "average_speed": 3.306,
    "max_speed": 4.5,
    "has_kudoed": false,
    "gear_id": "g0123456",
    "kilojoules": null,
    "average_watts": null,
    "device_watts": null,
    "max_watts": null,
    "weighted_average_watts": null
}
```

## Setup

The [Strava API Docs](https://developers.strava.com/docs/getting-started/) will be helpful.

1. If you have not already, go to https://www.strava.com/register and sign up for a Strava account.
2. After you are logged in, go to https://www.strava.com/settings/api and create an app.
3. You should see the “My API Application” page now.
4. When running strava_downloader.py for the first time, you'll need to enter the "Client ID" and "Client Secret" from this page. These will be stored in .env.
