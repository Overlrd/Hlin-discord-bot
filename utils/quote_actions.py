import logging
import json
import datetime
import requests

from pymongo import MongoClient
from settings import API_URL , MONGO_CONN_LINK

Client_Mongo = MongoClient(MONGO_CONN_LINK)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection


def get_quote():
  logging.info("utils-get_quote - getting quote from zenquotes.io")
  #make a get request to the zen quotes api
  response = requests.get(API_URL)
  #converting the response to json
  response_json = json.loads(response.text)
  #get the message with the key 'q' and the author with  the     key 'a'
  quote = response_json[0]['q'] + " -" + response_json[0]['a']
  return quote

## Get quote from Mongo db
def get_quote_from_db():
    logging.info("utils-get_quote_from_db - retrieving a random quote from mongo db ")
    #get random quote
    random = quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
    for i in random:
      quote = f"{i['quote']} - {i['author']}"
    return quote

async def post_quote(quote_text, quote_author):
  logging.info("utils-post_quote - add a new quote to mongodb")
  now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
  #quote_author = quote_author.split("@", 1)[1]
  doc = {"author":quote_author, "quote":quote_text, "date" : now}
  try :
    quotes_collection.insert_one(doc)
    logging.info("new quote added to db")
  except Exception as e:
    logging.error(e)