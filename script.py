#! /usr/bin/env python3

import random
from pymongo import MongoClient
from faker import Faker

DB_NAME = "library2"
N_PERSONS = 1000
N_BOOKS = 2000
N_LOANS = 3000

client = MongoClient()
db = client[DB_NAME]
persons = db["persons"]
books = db["books"]
loans = db["loans"]
fake = Faker(['ru_RU'])

for _ in range(N_PERSONS):

    person = dict()
    person['name'] = fake.name()
    person['address'] = fake.address()
    person['phone'] = fake.phone_number()
    person['passport'] = fake.random_int(min=10**9, max=10**10-1)#fake.passport_number()
    person['registration_date'] = fake.date_time_between()

    persons.insert_one(person)

for _ in range(N_BOOKS):

    book = dict()
    book['authors'] = [fake.name() for _ in range(fake.random_int(1, 2))]
    book['title'] = fake.catch_phrase()#f'Книга {fake.random_int(1, 100)}'
    book['genre'] = [f'Жанр {fake.random_int(1, 9)}' for _ in range(fake.random_int(1, 1))]
    book['isbn'] = fake.isbn13()
    books.insert_one(book)

persons = list(persons.find({}, {'_id': 1, 'name': 1}))
books = list(books.find({}, {'_id': 1, 'title': 1}))

for _ in range(N_LOANS - N_BOOKS // 2):
    
    loan = dict()
    person = random.choice(persons)
    loan['person_id'] = person['_id']
    loan['person_name'] = person['name']
    book = random.choice(books)
    loan['book_id'] = book['_id']
    loan['book_title'] = book['title']
    loan['issue_date'] = fake.date_time_between()
    loan['return_date'] = fake.date_time_between()
    loan['fact_return_date'] = fake.date_time_between()

    loans.insert_one(loan)

books = iter(books)
for _ in range(N_BOOKS // 2):
    
    loan = dict()

    person = random.choice(persons)
    loan['person_id'] = person['_id']
    loan['person_name'] = person['name']

    book = next(books)
    loan['book_id'] = book['_id']
    loan['book_title'] = book['title']

    loan['issue_date'] = fake.date_time_between()
    loan['return_date'] = fake.date_time_between()

    loans.insert_one(loan)