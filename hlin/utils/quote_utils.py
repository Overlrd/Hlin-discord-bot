import logging
import json
import datetime
import requests
from collections import namedtuple

from pymongo import MongoClient
from hlin.settings import API_URL , MONGO_CONN_LINK

Client_Mongo = MongoClient(MONGO_CONN_LINK)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection
Quote = namedtuple('quote',["author","content"])

def get_quote():
  logging.info("utils-get_quote - getting quote from zenquotes.io")
  response = requests.get(API_URL)
  response_json = json.loads(response.text)
  quote = response_json[0]['q'] + " - " + response_json[0]['a']
  return quote

def get_quote_from_db():
    logging.info("utils-get_quote_from_db - retrieving a random quote from mongo db ")
    random = quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
    for i in random:
      quote = f"{i['quote']} - {i['author']}"
    return quote

def post_quote(*args):
    now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
    if len(args) <= 1:
        for quote in args:
            doc = {"author":quote[0],"quote":quote[1], "date": now}
        try:
            quotes_collection.insert_one(doc)  
        except Exception as e:
            logging.error(e)      
    elif len(args) > 1:
        many_docs = []
        for quote in args:
            doc = {"author":quote[0],"quote":quote[1], "date": now}
            many_docs.append(doc)
        try :
            quotes_collection.insert_many(many_docs)
        except Exception as e:
            logging.error(e)
 