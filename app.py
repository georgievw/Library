
from faker import Faker
from flask import Flask
from markupsafe import escape
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/persons/")
def get_persons():
    client = MongoClient()
    db = client["library_test2"]
    persons = db["persons"]
    return list(persons.find()) 

@app.route("/test/")
def angrytest():
    angry_string = "<script>alert(\"bad\")</script>"
    #return f"<p>Hello, { escape(angry_string) } !</p>"
    return f"<p>Hello, {angry_string} !</p>"

@app.route("/test/<name>")
def test(name):
    return f"<p>Hello, {name}!</p>"

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
