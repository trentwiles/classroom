import os
import requests
import json
import datetime
import time
import sys

# This file reads the token created via oAuth in token.json, then uses the API

error_msg = "Please run demo2.py to create your tokens. Additionally, please check the scopes of the API based on what you will be doing."

def getToken(secure_id):
    if not os.path.exists("token-" + str(secure_id) + ".json"):
        print(error_msg)
        sys.exit()
    else:
        with open("token-" + str(secure_id) + ".json", 'r') as t:
            token = json.loads(t.read())["token"]
            return token


def getAllClasses(secure_id):
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken(secure_id))
    classIDs = []
    classNames = []
    for c in api.json()["courses"]:
        classIDs.append(c["id"])
        classNames.append(c["name"])
    return {"ids": classIDs, "names": classNames}

def getClassByID(id, secure_id):
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken(secure_id))
    for c in api.json()["courses"]:
        if int(c["id"]) == id:
            return c

def getIDfromName(name, secure_id):
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken(secure_id))
    for c in api.json()["courses"]:
        if c["name"] == name:
            return c["id"]
    return None

def getCourseLoadByID(id, secure_id):
    api = requests.get("https://classroom.googleapis.com/v1/courses/" + str(id) + "/courseWork?access_token=" + getToken(secure_id))
    return api.json()

def getCourseLoadByName(name, secure_id):
    id = getIDfromName(name, secure_id)
    if id != None:
        api = requests.get("https://classroom.googleapis.com/v1/courses/" + str(id) + "/courseWork?access_token=" + getToken(secure_id))
        return api.json()
    return None