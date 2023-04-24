import os
import requests
import json
import datetime
import time
import sys

# This file reads the token created via oAuth in token.json, then uses the API

error_msg = "Please run demo2.py to create your tokens. Additionally, please check the scopes of the API based on what you will be doing."

def getToken():
    if not os.path.exists("token.json"):
        print(error_msg)
        sys.exit()
    else:
        with open("token.json", 'r') as t:
            token = json.loads(t.read())["token"]
            return token


def getAllClasses():
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken())
    classIDs = []
    classNames = []
    for c in api.json()["courses"]:
        classIDs.append(c["id"])
        classNames.append(c["name"])
    return {"ids": classIDs, "names": classNames}

"""
api = requests.get("https://classroom.googleapis.com/v1/courses/538643163021/courseWork?access_token=" + getToken())
if api.status_code != 200:
    print(error_msg)
    sys.exit()
print("This is the work you have to do:")
for c in api.json()["courseWork"]:
    print(c["title"])
    #print(c)
    # I had to looks this up, this replaces the weird date format Google provides with the
    # epoch time so I can work with it
    time_obj = datetime.datetime.fromisoformat(c["creationTime"].replace('Z', '+00:00'))
    epoch_time = int(time_obj.timestamp())
    time_now = int(time.time())

    age = time_now - epoch_time

    due_at = int(datetime.datetime(c["dueDate"]["year"], c["dueDate"]["month"], c["dueDate"]["day"]).timestamp())
    print(c["dueDate"]["year"], c["dueDate"]["month"], c["dueDate"]["day"])
    if (time_now - due_at) >= 0:
        print("=== THIS IS LATE ===")
    print("This was posted " + str(round(age/3600/24, 1)) + " days ago")
    """