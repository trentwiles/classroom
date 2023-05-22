import email-test
import os
import sys
import json
from datetime import datetime, date


# should be run every hour

if os.path.exists('temp/settings.json') == False:
    print("Please ensure the settings.json file exists")
    sys.exit()

email_time = ""

with open('temp/settings.json') as s:
    api = json.loads(s.read())
    email_time = api["email"]

today = date.today()
datetime_str = f"{today} {email_time}"
datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

if int(datetime_obj.timestamp()) < 3600:
    email-test.send_email()