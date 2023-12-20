from flask import Flask, render_template, request
from pymongo import MongoClient
from bson import ObjectId

DB_NAME = "library"

app = Flask(__name__)
client = MongoClient()
db = client[DB_NAME]
persons = db["persons"]
books = db["books"]

@app.route("/persons/")
def get_persons():
    name = request.args.get('name')
    if name:
        data = persons.find({'name': {'$regex': name, '$options': '$i' }})
    else:
        data = persons.find() 
    return render_template('persons.html', persons=data)

@app.route("/books/")
def get_books():
    title = request.args.get('title')
    if title:    
        data = books.find({'title': {'$regex': title, '$options': '$i' }})
    else:
        data = books.find()
    return render_template('books.html', books=data)

@app.route("/persons/<id>")
def get_person(id):
    data = persons.find_one({"_id": ObjectId(id)})
    return render_template('person.html', person=data) 

@app.route("/books/<id>")
def get_book(id):
    data = books.find_one({"_id": ObjectId(id)})
    return render_template('book.html', book=data)