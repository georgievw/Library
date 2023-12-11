from pymongo import MongoClient
from faker import Faker
from datetime import date, datetime, timedelta, timezone

DB_NAME = "library_test2"
N_PERSONS = 10
N_BOOKS = 10


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
    person['open_deals'] = {}
    
    person['closed_deals'] = {}

    persons.insert_one(person)

for _ in range(N_BOOKS):
    book = dict()

    n_authors = fake.random_int(1, 2)
    author_lst = [fake.name() for _ in range(n_authors)]
    book['authors'] = author_lst

    book['title'] = ' '.join(fake.words(fake.random_int(1, 5)))

    book['tags'] = ['Шла', 'Саша', 'Шоссе']

    book['open_deal'] = {}

    book['closed_deals'] = {}
    books.insert_one(book)
