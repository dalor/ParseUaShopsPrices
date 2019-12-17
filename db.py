import os
from pymongo import MongoClient

url = os.environ.get('MONGODB_URI')

client = MongoClient(url)

db = client.heroku_06hf45qq