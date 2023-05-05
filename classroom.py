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

def getClassByID(id):
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken())
    for c in api.json()["courses"]:
        if int(c["id"]) == id:
            return c

def getIDfromName(name):
    api = requests.get("https://classroom.googleapis.com/v1/courses?access_token=" + getToken())
    for c in api.json()["courses"]:
        if c["name"] == name:
            return c["id"]
    return None

def getCourseLoadByID(id):
    api = requests.get("https://classroom.googleapis.com/v1/courses/" + str(id) + "/courseWork?access_token=" + getToken())
    return api.json()

def getCourseLoadByName(name):
    id = getIDfromName(name)
    if id != None:
        api = requests.get("https://classroom.googleapis.com/v1/courses/" + str(id) + "/courseWork?access_token=" + getToken())
        return api.json()
    return None