from discord.ext import commands
from pymongo import MongoClient
import requests
import json
import os 


class QuoteCog(commands.cog):
    def __init__(self, bot):
        """ SETUP CONNECTION WITH MONGODB """
        MONGO_CONN_LINK =  os.environ['CONN_LINK']
        Client_Mongo = MongoClient(MONGO_CONN_LINK)
        quotes_db = Client_Mongo.quotes
        self.quotes_collection = quotes_db.quotes_collection
        """GOOGLE PERSCEPCTIVE API KEY AND ZENQUOTES ROUTE"""
        self.ZENQUOTES_API_URL = 'https://zenquotes.io/api/random'
        PERSPECTIVE_API = os.environ['G_PER_TOKEN']
        """BOT"""
        self.bot = bot 

    def get_quote(self):
        #make a get request to the zen quotes api
        response = requests.get(self.ZENQUOTES_API_URL)
        #converting the response to json
        response_json = json.loads(response.text)
        #get the message with the key 'q' and the author with  the key 'a'
        quote = response_json[0]['q'] + " -" + response_json[0]['a']
        return quote

