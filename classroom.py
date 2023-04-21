import os
import requests
import json

# This file reads the token created via oAuth in token.json, then uses the API

if not os.path.exists("token.json"):
    print("Please run demo2.py to create your tokens. Additionally, please check the scopes of the API based on what you will be doing.")
else:
    with open("token.json", 'r') as t:
        token = json.loads(t.read())["token"]
        print(token)
        api = requests.get("https://classroom.googleapis.com/v1/courses/538643163021/courseWork?access_token=" + token)
        for c in api.json()["courseWork"]:
            print(c["title"])