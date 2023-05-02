import os
import classroom
import json
import openai
from dotenv import load_dotenv
import weasyprint

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
    chatGPTprompt = "Assuming that math typically has the most homework, next science/physics, then english, then foreign languages, then electives, how would this list of class titles rank? Please list them in order, one per line, no other text. Thanks! Here is the list: \n"
    if not os.path.isfile('temp/classes.json') or not os.path.isfile('temp/settings.json'):
        return Exception(FileNotFoundError)
    with open('temp/classes.json') as r:
        s = json.loads(r.read())
        for x in s:
            if x != None:
                n = classroom.getClassByID(int(x))["name"]
                chatGPTprompt += n + "\n"
    response = chatGPT(chatGPTprompt)
    for orderedClass in response.split("\n"):
        print("30 minutes for " + orderedClass)
        print()