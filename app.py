from flask import Flask, render_template, request
from pymongo import MongoClient
from bson import ObjectId

DB_NAME = "new_library_test5"

app = Flask(__name__)
client = MongoClient()
db = client[DB_NAME]
persons = db["persons"]
books = db["books"]
loans = db["loans"]

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
    data['open_loans'] = list(loans.find({"person_id": ObjectId(id), "fact_return_date": {"$exists": False}}, {"person_id": 0, "person_name": 0}))
    data['closed_loans'] = list(loans.find({"person_id": ObjectId(id), "fact_return_date": {"$exists": True}}, {"person_id": 0, "person_name": 0}))
    return render_template('person.html', person=data) 

@app.route("/books/<id>")
def get_book(id):
    data = books.find_one({"_id": ObjectId(id)})
    data['open_loan'] = loans.find_one({"book_id": ObjectId(id), "fact_return_date": {"$exists": False}}, {"book_id": 0, "book_title": 0})
    data['closed_loans'] = list(loans.find({"book_id": ObjectId(id), "fact_return_date": {"$exists": True}}, {"book_id": 0, "book_title": 0}))
    print(data)
    return render_template('book.html', book=data)