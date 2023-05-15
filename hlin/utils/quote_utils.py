import logging
import json
import datetime
import requests 
from collections import namedtuple

from pymongo import MongoClient
from config import Settings , ZENQUOTES_API_URL
settings = Settings()

Client_Mongo = MongoClient(settings.mongodb_conn_link)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection
Quote = namedtuple('quote',["author","content"])

def get_quote():
  response = requests.get(ZENQUOTES_API_URL)
  response_json = json.loads(response.text)
  quote = response_json[0]['q'] + " - " + response_json[0]['a']
  return quote

def get_quote_from_db():
    random = quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
    for i in random:
      quote = f"{i['quote']} - {i['author']}"
    return quote

def post_quote(*args:tuple):
    """post quote takes one or multiple tuples formated as (author,quote)"""
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
 