import discord 
from discord.ext import commands 
import os 
import requests
import json
from discord import app_commands
from pymongo import MongoClient
from datetime import datetime

import pprint
# import db 

# API URL
API_URL = 'https://zenquotes.io/api/random'


## set up the bot 
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())

## set up  mongo db 
MONGO_CONN_LINK = my_secret = os.environ['CONN_LINK']
Client_Mongo = MongoClient(MONGO_CONN_LINK)

quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection

res_mongo = quotes_collection.find()
printer = pprint.PrettyPrinter()

for i in res_mongo:
  printer.pprint(i)


## get quotes 
def get_quote():
  #make a get request to the zen quotes api
  response = requests.get(API_URL)
  #converting the response to json
  response_json = json.loads(response.text)
  
  #get the message with the key 'q' and the author with  the     key 'a'
  quote = response_json[0]['q'] + " -" + response_json[0]['a']
  return quote





def post_quote(quote_text, quote_author):
  now = datetime.now().strftime("%y:%m:%d:%H:%M:%S")
  #quote_author = quote_author.split("@", 1)[1]
  doc = {"author":quote_author, "quote":quote_text, "date" : now}
  try :
    quotes_collection.insert_one(doc)
    print("quote sended ")
  except Exception as e:
    print(e)
  




@bot.event 
async def on_ready():
    print(f'--------------------Logged--------------')

    try:
        synced = await bot.tree.sync()
        print(f" {len(synced)} commands synced " )
    except Exception as e :
      print(e)
      
  
      
## main func 

      
@bot.tree.command(name = "inspire")
async def inspire(interaction : discord.Interaction):
    quote = get_quote()
    await interaction.response.send_message(quote, ephemeral = True )



@bot.tree.command(name = "add_quote")
async def add_quote(interaction : discord.Interaction , quote: str):
  await interaction.response.send_message(f"{quote} by  {interaction.user.mention} ", ephemeral = True)
  print(interaction.user)
  post_quote(quote, str(interaction.user))
    
    

bot.run(TOKEN)