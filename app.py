from flask import Flask, render_template
from markupsafe import escape
from pymongo import MongoClient
from bson import ObjectId, json_util
import json

app = Flask(__name__)
client = MongoClient()
db = client["library_test8"]
persons = db["persons"]
books = db["books"]

@app.route("/persons/")
def get_persons():
    data = persons.find() 
    return render_template('persons.html', persons=data)

@app.route("/books/")
def get_books():
    data = books.find()
    return render_template('books.html', books=data)

@app.route("/persons/<id>")
def get_person(id):
    data = persons.find_one({"_id": ObjectId(id)})
    return render_template('person.html', person=data) 
#json.loads(json_util.dumps(data)) 

@app.route("/books/<id>")
def get_book(id):
    data = books.find_one({"_id": ObjectId(id)})
    return render_template('book.html', book=data)
    # return json.loads(json_util.dumps(data)) 


