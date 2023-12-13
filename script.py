#! /usr/bin/env python3

import random
from pymongo import MongoClient
from faker import Faker
from datetime import date, datetime, timedelta, timezone

DB_NAME = "library_test8"
N_PERSONS = 5
N_BOOKS = 10
N_CLOSED_DEALS = 10
N_OPEN_DEALS = 5

client = MongoClient()
db = client[DB_NAME]
persons = db["persons"]
books = db["books"]

fake = Faker(['ru_RU'])
offset = 1
for _ in range(N_PERSONS):
    person = dict()
    person['name'] = fake.name()
    person['address'] = fake.address()
    person['phone'] = fake.phone_number()
    person['passport'] = fake.passport_number()
    person['registration_date'] = fake.date_time_between()
    #datetime.now(tz=timezone.utc)#datetime.combine(fake.passport_dob(), datetime.min.time())
    
    person['open_deals'] = []
    
    person['closed_deals'] = []

    persons.insert_one(person)

for _ in range(N_BOOKS):
    book = dict()

    n_authors = fake.random_int(1, 2)
    author_lst = [fake.name() for _ in range(n_authors)]
    book['authors'] = author_lst

    book['title'] = ' '.join(fake.words(fake.random_int(1, 5)))

    book['tags'] = ['Шла', 'Саша', 'Шоссе']

    # book['open_deal'] = {}

    book['closed_deals'] = []
    books.insert_one(book)

close_deal_persons = list(persons.find())
close_deal_books = list(books.find())
for _ in range(N_CLOSED_DEALS):
    book = random.choice(close_deal_books)
    person = random.choice(close_deal_persons)
    
    deal = dict()
    deal['issue_date'] = datetime.now()
    deal['return_date'] = datetime.now()
    deal['fact_return_date'] = datetime.now()

    book_deal = deal.copy()
    book_deal['people_id'] = person['_id']
    book_deal['person_name'] = person['name']

    person_deal = deal
    person_deal['book_id'] = book['_id']
    person_deal['book_title'] = book['title']

    persons.update_one({'_id': person['_id']}, {'$addToSet': {'closed_deals': person_deal}})
    books.update_one({'_id': book['_id']}, {'$addToSet': {'closed_deals': book_deal}})

open_deal_persons = list(persons.find())
for _ in range(min(N_OPEN_DEALS, N_BOOKS)):
    person = random.choice(open_deal_persons)
    book = books.find_one({'open_deal': None}) 

    deal = dict()
    deal['issue_date'] = datetime.now()
    deal['return_date'] = datetime.now()

    book_deal = deal.copy()
    book_deal['person_id'] = person['_id']
    book_deal['person_name'] = person['name']

    person_deal = deal
    person_deal['book_id'] = book['_id']
    person_deal['book_title'] = book['title']

    persons.update_one({'_id': person['_id']}, {'$addToSet': {'open_deals': person_deal}})
    books.update_one({'_id': book['_id']}, {'$set': {'open_deal': book_deal}})


