from flask import Flask, Response, render_template, request, url_for, redirect
import sys, flask
import httpagentparser
import classroom
import json
import os

app = Flask(__name__)

GLOBAL_VERSION = "0.0.1 alpha"

@app.route('/')
def index():
    return render_template("index.html", version=GLOBAL_VERSION)

# First, the user selects what classes they want
@app.route('/step1')
def s1():
    if os.path.exists('temp/classes.json'):
        return redirect(url_for('s2'))
    # To do this, I needed to include Python's enumerate function.
    # https://paste.gg/p/anonymous/4c94ffb214e14e5187cd51c19fea80b9
    return render_template("selectClasses.html", version=GLOBAL_VERSION, classes=classroom.getAllClasses(), enumerate=enumerate)

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
    if os.path.exists('temp/settings.json'):
        return redirect(url_for('dash'))
    return render_template("tolerance.html", version=GLOBAL_VERSION)

@app.route('/api/v1/tolerance', methods=["POST"])
def a2():
    email = request.form.get('email')
    late = request.form.get('late')
    selected = request.form.get('selectedTime')
    with open('temp/settings.json', 'a') as w:
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
    with open('temp/settings.json', 'r') as r:
        contents = json.loads(r)
        r.close()
    
    contents[item] = newValue

    with open('temp/settings.json', 'w') as w:
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

    if not os.path.exists('temp/settings.json') or not os.path.exists('temp/classes.json'):
        return redirect("/?missing_configuration=1")
    
    classes = 0
    with open('temp/classes.json', 'r') as r:
        for x in r.readlines():
            classes += 1
        r.close()

    email = ""
    tol = ""
    dTime = ""
    with open('temp/settings.json', 'r') as r:
        api = json.load(r)
        email = api["email"]
        tol = api["late"]
        dTime = api["selected"]
    name = "Trent"

    return render_template("dashboard.html", name=name, version=GLOBAL_VERSION, numClasses = classes, email=email, tolerance=tol, lateTime=dTime)

@app.route('/debug')
def debug():
    return render_template('debug.html', version=GLOBAL_VERSION, python=sys.version, flask_v=flask.__version__, ip=request.environ['REMOTE_ADDR'], ua=httpagentparser.detect(request.headers.get('User-Agent')), connected_via=request.scheme.upper())

if __name__ == '__main__':
    app.run(debug=True)
