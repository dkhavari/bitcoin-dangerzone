from libraries.alchemy.alchemyapi import AlchemyAPI
import requests
import pymongo
from pymongo import MongoClient

# --------------------------------------------------
# Connect with the remote Mongo and prepare NLP API.
# --------------------------------------------------
client = MongoClient('ds047571.mongolab.com:47571')
db = client.coinage
db.authenticate('bit', 'coin')
collection = db['articles']
api = AlchemyAPI()

# Logic.

#collection.save({'title': 'King of Thebes'})
#print collection.find_one()
#response = api.sentiment("text", "Life is good.")
#print response