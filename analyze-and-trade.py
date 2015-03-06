import datetime
import pymongo as pymongo
from pymongo import MongoClient


# Constants.
MAX_ARTICLES = 250

# --------------------------------------------------
# Connect with the remote Mongo and prepare NLP API.
# --------------------------------------------------
client = MongoClient('ds047571.mongolab.com:47571')
db = client.coinage
db.authenticate('bit', 'coin')
collection = db['articles']

# Get a healthy number of articles to ensure we have enough.
articles = collection.find().sort("date",pymongo.DESCENDING).limit(MAX_ARTICLES)


print articles.count(with_limit_and_skip=True)