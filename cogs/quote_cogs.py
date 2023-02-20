import discord
from discord.ext import commands
from pymongo import MongoClient
import requests
import datetime
import json
import os 


class QuoteCog(commands.Cog):
    def __init__(self, bot):
        print('cog loaded here ')
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

    """LOAD RANDOM QUOTE FROM ZENQUOTES API"""
    def get_quote(self):
        #make a get request to the zen quotes api
        response = requests.get(self.ZENQUOTES_API_URL)
        #converting the response to json
        response_json = json.loads(response.text)
        #get the message with the key 'q' and the author with  the key 'a'
        quote = response_json[0]['q'] + " -" + response_json[0]['a']
        return quote
    
    """LOAD RANDOM QUOTE FROM MONDODB"""
    def get_quote_from_db(self):
        #get random q
        random = self.quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
        for i in random:
            quote = f"{i['quote']} -{i['author']}"
        return quote
    
    """POST A QUOTE TO MONGODB"""
    def post_quote(self, quote_text, quote_author):
        now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
        #quote_author = quote_author.split("@", 1)[1]
        doc = {"author":quote_author, "quote":quote_text, "date" : now}
        try :
            self.quotes_collection.insert_one(doc)
            print("quote sended ")
        except Exception as e:
            print(e)

    @commands.command(name = "inspire", description="Get a quote")
    async def inspire(self, ctx):
        #quote = get_quote()
        quote = self.get_quote_from_db()
        await ctx.response.send_message(quote)


async def setup(bot):
    await bot.add_cog(QuoteCog(bot))






    


