from flask import Flask, Response, render_template, request
import sys, flask
import httpagentparser
import classroom
import json

app = Flask(__name__)

GLOBAL_VERSION = "0.0.1 alpha"

@app.route('/')
def index():
    return render_template("index.html", version=GLOBAL_VERSION)

@app.route('/step1')
def s1():
    # To do this, I needed to include Python's enumerate function.
    # https://paste.gg/p/anonymous/4c94ffb214e14e5187cd51c19fea80b9
    return render_template("selectClasses.html", version=GLOBAL_VERSION, classes=classroom.getAllClasses(), enumerate=enumerate)

# API route to go along with step one
@app.route('/api/v1/selectClasses', methods=["POST"])
def a1():
    c = request.form.get('classes')
    classesPicked = [int(num) for num in c.split(",")] # convert the string of "1, 2, 3, 4" into an array
    #print(c)
    return Response(json.dumps({"message": "ok"}), content_type="application/json"), 200


@app.route('/dashboard')
def dash():
    # THIS IS ALL DEMO DATA
    # CHANGE THIS ONCE THERE IS ACCESS TO THE
    # CLASSROOM API

    name = "Trent"

    return render_template("dashboard.html", name=name, version=GLOBAL_VERSION)

@app.route('/debug')
def debug():
    return render_template('debug.html', version=GLOBAL_VERSION, python=sys.version, flask_v=flask.__version__, ip=request.environ['REMOTE_ADDR'], ua=httpagentparser.detect(request.headers.get('User-Agent')))

if __name__ == '__main__':
    app.run(debug=True)