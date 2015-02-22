from libraries.alchemy.alchemyapi import AlchemyAPI
import requests
import datetime
import pymongo
from pymongo import MongoClient
import pipeline


# --------------------------------------------------
# Connect with the remote Mongo and prepare NLP API.
# --------------------------------------------------
client = MongoClient('ds047571.mongolab.com:47571')
db = client.coinage
db.authenticate('bit', 'coin')
collection = db['articles']
api = AlchemyAPI()

# Logic.
articles = pipeline.get_articles()

for article in articles:
	date = datetime.datetime.strptime(str(article[0]), '%a %Y-%m-%d %H:%M:%S')
	url = article[1]
	engagement = float(article[2])
	text = article[3]
	
	# print '\n\n\n\n\n'
	# print date
	# print url
	# print engagement
	# print text

	# nlp_sentiment = api.sentiment("text", text)
	# score = nlp_sentiment['docSentiment']['score']

	print url
	# print score

	# quit()



#collection.save({'title': 'King of Thebes'})
#print collection.find_one()
#response = api.sentiment("text", "Life is good.")
#print response