#! /usr/bin/env python3

import random
from pymongo import MongoClient
from faker import Faker

DB_NAME = "library"
N_PERSONS = 10
N_BOOKS = 20
N_CLOSED_DEALS = 30
N_OPEN_DEALS = 10

client = MongoClient()
db = client[DB_NAME]
persons = db["persons"]
books = db["books"]
fake = Faker(['ru_RU'])

for _ in range(N_PERSONS):

    person = dict()
    person['name'] = fake.name()
    person['address'] = fake.address()
    person['phone'] = fake.phone_number()
    person['passport'] = fake.passport_number()
    person['registration_date'] = fake.date_time_between()
    person['open_deals'] = []
    person['closed_deals'] = []

    persons.insert_one(person)

for _ in range(N_BOOKS):

    book = dict()
    book['authors'] = [fake.name() for _ in range(fake.random_int(1, 2))]
    book['title'] = f'Книга {fake.random_int(1, 100)}'
    book['tags'] = [f'Тема {fake.random_int(1, 10)}' for _ in range(fake.random_int(1, 3))]
    book['closed_deals'] = []

    books.insert_one(book)

close_deal_persons = list(persons.find())
close_deal_books = list(books.find())
for _ in range(N_CLOSED_DEALS):
    book = random.choice(close_deal_books)
    person = random.choice(close_deal_persons)
    
    deal = dict()
    deal['issue_date'] = fake.date_time_between()
    deal['return_date'] = fake.date_time_between()
    deal['fact_return_date'] = fake.date_time_between()

    book_deal = deal.copy()
    book_deal['person_id'] = person['_id']
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
    deal['issue_date'] = fake.date_time_between()
    deal['return_date'] = fake.date_time_between()

    book_deal = deal.copy()
    book_deal['person_id'] = person['_id']
    book_deal['person_name'] = person['name']

    person_deal = deal
    person_deal['book_id'] = book['_id']
    person_deal['book_title'] = book['title']

    persons.update_one({'_id': person['_id']}, {'$addToSet': {'open_deals': person_deal}})
    books.update_one({'_id': book['_id']}, {'$set': {'open_deal': book_deal}})


