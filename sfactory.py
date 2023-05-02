import os
import classroom
import json

def createS():
    if not os.path.isfile('temp/classes.json') or not os.path.isfile('temp/settings.json'):
        return Exception(FileNotFoundError)
    with open('temp/classes.json') as r:
        s = json.loads(r.read())
        for x in s:
            if x != None:
                print(x)