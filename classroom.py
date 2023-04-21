import os
import requests
import json
import datetime
import time
import sys

# This file reads the token created via oAuth in token.json, then uses the API

error_msg = "Please run demo2.py to create your tokens. Additionally, please check the scopes of the API based on what you will be doing."

if not os.path.exists("token.json"):
    print(error_msg)
else:
    with open("token.json", 'r') as t:
        token = json.loads(t.read())["token"]
        print(token)
        api = requests.get("https://classroom.googleapis.com/v1/courses/538643163021/courseWork?access_token=" + token)
        if api.status_code != 200:
            print(error_msg)
            sys.exit()
        print("This is the work you have to do:")
        for c in api.json()["courseWork"]:
            print(c["title"])
            # I had to looks this up, this replaces the weird date format Google provides with the
            # epoch time so I can work with it
            time_obj = datetime.datetime.fromisoformat(c["creationTime"].replace('Z', '+00:00'))
            epoch_time = int(time_obj.timestamp())
            time_now = int(time.time())

            age = time_now - epoch_time
            print("This was posted " + str(round(age/3600/24, 1)) + " days ago")