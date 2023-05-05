import os
import classroom
import json
import openai
from dotenv import load_dotenv
import weasyprint
import datetime
import time

load_dotenv()

def chatGPT(message):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": message}
    ]
    )

    return completion.choices[0].message["content"]


def createS():
    # Step One: Set up the chatGPT prompt
    chatGPTprompt = "Assuming that math typically has the most homework, next science/physics, then english, then foreign languages, then electives, how would this list of class titles rank? Please list them in order, one per line, no other text. Thanks! Here is the list: \n"
    # Step Two: Check if the configuration files set up before the dashboard is accessed exist
    if not os.path.isfile('temp/classes.json') or not os.path.isfile('temp/settings.json'):
        return Exception(FileNotFoundError)
    # Step Three: Open the classes file. This contains all of the class IDs
    with open('temp/classes.json') as r:
        s = json.loads(r.read())
        for x in s:
            if x != None:
                n = classroom.getClassByID(int(x))["name"]
                # Step Four: add each class name to the ChatGPT prompt so they can be ordered
                chatGPTprompt += n + "\n"
    print(chatGPTprompt)
    time.sleep(60)
    response = chatGPT(chatGPTprompt)
    for orderedClass in response.split("\n"):
        print("30 minutes for " + orderedClass)
        for x in classroom.getCourseLoadByName(orderedClass)["courseWork"]:
            # Step Five: Now fetch all of the course work for each class
            dueAt = int(datetime.datetime(x["dueDate"]["year"], x["dueDate"]["month"], x["dueDate"]["day"]).timestamp())
            timeNow = int(time.time())
            print(timeNow - dueAt)