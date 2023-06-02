from flask import Flask, Response, render_template, request, url_for, redirect, send_file, session, make_response
import sys, flask
import httpagentparser
import classroom
import json
import os
import sfactory
from google_auth_oauthlib.flow import Flow
import random
import requests
#import demo2

# this doesn't work for some weird reason
# 
SCOPES = ['https://www.googleapis.com/auth/classroom.student-submissions.me.readonly', 'https://www.googleapis.com/auth/classroom.courses.readonly']

app = Flask(__name__)

GLOBAL_VERSION = "0.0.3 beta"

app.secret_key = os.getenv("SECRET")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

@app.route('/')
def index():
    return render_template("index.html", version=GLOBAL_VERSION)

"""
GOOGLE OAUTH LOGIN CONTENT STARTS HERE
"""

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri=url_for('callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session.pop('state', '')
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    try:
        os.remove("token.json")
    except:
        print("couldn't remove it :(")
    
    RANDOM_SECURE_SESSION_ID = random.randint(100000,10000000000)

    with open('token-' + str(RANDOM_SECURE_SESSION_ID) + '.json', 'a') as t:
        t.write(json.dumps({"token": credentials.token}))
    # Store the credentials or use them to make API requests
    resp = make_response(render_template("home.html"))
    resp.set_cookie('RANDOM_SECURE_SESSION_ID', str(RANDOM_SECURE_SESSION_ID))

    return resp



"""
GOOGLE OAUTH LOGIN CONTENT ENDS HERE
"""

# First, the user selects what classes they want
@app.route('/step1')
def s1():
    if os.path.exists('temp/classes.json'):
        return redirect(url_for('s2'))
    # To do this, I needed to include Python's enumerate function.
    # https://paste.gg/p/anonymous/4c94ffb214e14e5187cd51c19fea80b9
    return render_template("selectClasses.html", version=GLOBAL_VERSION, classes=classroom.getAllClasses(request.cookies.get("RANDOM_SECURE_SESSION_ID")), enumerate=enumerate)

# API route to go along with step one
@app.route('/api/v1/selectClasses', methods=["POST"])
def a1():
    if os.path.exists('temp/classes.json'):
        return redirect(url_for('dash'))
    c = request.form.get('classes')
    classesPicked = [int(num) for num in c.split(",")] # convert the string of "1, 2, 3, 4" into an array
    #print(c)
    with open('temp/classes.json', 'a') as w:
        w.write(json.dumps(classesPicked))
        w.close()
    return Response(json.dumps({"message": "ok"}), content_type="application/json"), 200

@app.route('/step2')
def s2():
    if os.path.exists('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json'):
        return redirect(url_for('dash'))
    return render_template("tolerance.html", version=GLOBAL_VERSION)

@app.route('/api/v1/tolerance', methods=["POST"])
def a2():
    email = request.form.get('email')
    late = request.form.get('late')
    selected = request.form.get('selectedTime')
    with open('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json', 'a') as w:
        w.write(json.dumps({"email": email, "selected": selected[0] + ":" + selected[1] + selected[2], "late": late}))
    return Response(json.dumps({"message": "ok"}), content_type="application/json"), 200

@app.route('/api/v1/quickSave', methods=["POST"])
def quickSave():
    item = request.form.get('item')
    newValue = request.form.get('value')
    settings_settings = ["email", "selected", "late"]
    valid = False
    for x in settings_settings:
        if item == x:
            valid = True
    if valid == False:
        return Response(json.dumps({"message": "Invalid setting change attempt: setting '" + str(item) + "' does not exist"}), content_type="application/json"), 400
    contents = ""
    with open('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json', 'r') as r:
        contents = json.loads(r)
        r.close()
    
    contents[item] = newValue

    with open('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json', 'w') as w:
        w.write(json.dumps(contents))
        w.close()
    
    return Response(json.dumps({"message": "ok"}), content_type="application/json"), 200

# Debugging route to reset everything
@app.route('/reset')
def reset():
    for f in os.listdir('temp'):
        if f != ".gitignore":
            os.remove('temp/' + f)
            print("deleted temp/" + f)
    return "OK"

@app.route('/dashboard')
def dash():
    # THIS IS ALL DEMO DATA
    # CHANGE THIS ONCE THERE IS ACCESS TO THE
    # CLASSROOM API

    if not os.path.exists('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json') or not os.path.exists('temp/classes.json'):
        return redirect("/?missing_configuration=1")
    
    classes = 0
    with open('temp/classes.json', 'r') as r:
        for x in r.readlines():
            classes += 1
        r.close()

    email = ""
    tol = ""
    dTime = ""
    with open('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json', 'r') as r:
        api = json.load(r)
        email = api["email"]
        tol = api["late"]
        dTime = api["selected"]
    name = "Trent"

    return render_template("dashboard.html", name=name, version=GLOBAL_VERSION, numClasses = classes, email=email, tolerance=tol, lateTime=dTime)

@app.route('/debug')
def debug():
    print(session.items())
    if request.headers.get('X-Forwarded-For') != None:
        ip = request.headers.get('X-Forwarded-For')
    else:
        ip = request.environ['REMOTE_ADDR']
    return render_template('debug.html', version=GLOBAL_VERSION, python=sys.version, flask_v=flask.__version__, ip=ip, ua=httpagentparser.detect(request.headers.get('User-Agent')), connected_via=request.scheme.upper())

@app.route("/s.pdf")
def s():
    if os.path.exists('output.pdf'):
        os.remove('output.pdf')
    
    if not os.path.exists('temp/settings-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.json'):
        return redirect('/')
    
    sfactory.assemble(sfactory.createS(str(request.cookies.get("RANDOM_SECURE_SESSION_ID"))))

    return send_file('output-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.pdf')

@app.route("/api/v1/export")
def export():
    # gofile doesn't have a login req for the API, so a token/key isn't needed
    if not os.path.exists('output-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.pdf'):
        return Response("400 Bad Request", content_type="text/plain"), 400
    with open('output-' + str(request.cookies.get("RANDOM_SECURE_SESSION_ID")) + '.pdf') as fi:
        files = {'file': fi}
    
    server = requests.get("https://api.gofile.io/getServer").json()["data"]["server"]

    r = requests.post("https://" + server + ".gofile.io/uploadFile", files=files)
    return Response(r.json()["data"]["downloadPage"], content_type="text/plain"), 200

if __name__ == '__main__':
    app.run(debug=True)
