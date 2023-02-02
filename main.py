import discord 
from discord.ext import commands 
from discord.ext.commands import CommandNotFound
import interactions
from googleapiclient import discovery
import os 
import requests
import json
from discord import app_commands
from pymongo import MongoClient
from datetime import datetime
# e load env variables
from dotenv import load_dotenv
load_dotenv()
## import google perspective
from g_perspective import perspective_client , PERSPECTIVE_API
my_perspective_client = perspective_client(PERSPECTIVE_API)

# API URL
API_URL = 'https://zenquotes.io/api/random'


## set up the bot 
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())

## set up  mongo db 
MONGO_CONN_LINK =  os.environ['CONN_LINK']
Client_Mongo = MongoClient(MONGO_CONN_LINK)


quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection

res_mongo = quotes_collection.find()
#printer = pprint.PrettyPrinter()

def get_quote():
  #make a get request to the zen quotes api
  response = requests.get(API_URL)
  #converting the response to json
  response_json = json.loads(response.text)
  
  #get the message with the key 'q' and the author with  the     key 'a'
  quote = response_json[0]['q'] + " -" + response_json[0]['a']
  return quote


def get_quote_from_db():
    #get random q
    random = quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
    for i in random:
      quote = f"{i['quote']} -{i['author']}"
    return quote


def config_dayly_quotes(user_id, is_dayly_activate , hour, filename="config.json" ):
  dic = {
    "user": user_id,
    "dayly":is_dayly_activate,
    "when":hour}

  with open(filename, "r+") as file :
    file_data = json.load(file)
    print(file_data)
    for i in file_data['dayly_quotes_config']:
      print(i['user'])
    file_data['dayly_quotes_config'].append(dic)
    file.seek(0)
    json.dump(file_data, file, indent=4)

def post_quote(quote_text, quote_author):
  now = datetime.now().strftime("%y:%m:%d:%H:%M:%S")
  #quote_author = quote_author.split("@", 1)[1]
  doc = {"author":quote_author, "quote":quote_text, "date" : now}
  try :
    quotes_collection.insert_one(doc)
    print("quote sended ")
  except Exception as e:
    print(e)

class My_Button(discord.ui.View):
  def __init__(self):
    super().__init__()
  @discord.ui.button(label="Activate", style= discord.ButtonStyle.primary)
  async def activate(self ,interaction : discord.Interaction, button : discord.ui.Button ):
    #await interaction.user.send("you clicked me ")      
    await interaction.response.send_message("Morning Quotes activated")

  @discord.ui.button(label="Deactivate", style= discord.ButtonStyle.danger)
  async def deactivate(self ,interaction : discord.Interaction, button : discord.ui.Button ):
    #await interaction.user.send("you clicked me ")      
    await interaction.response.send_message("Morning quotes deactivated")

  

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
      em = discord.Embed(title=f"Sorry :-( ", description=f"I Don't support this command.", color=ctx.author.color) 
      await ctx.send(embed=em, ephemeral = True, mention_author = True)


@bot.event 
async def on_ready():
    print(f'--------------------Logged--------------')

    try:
        synced = await bot.tree.sync()
        print(f" {len(synced)} commands synced " )
    except Exception as e :
      print(e)
      

## main func 

      
@bot.tree.command(name = "inspire", description="Get a quote")
async def inspire(interaction : discord.Interaction):
    #quote = get_quote()
    quote = get_quote_from_db()
    await interaction.response.send_message(quote, ephemeral = True )



@bot.tree.command(name = "add_quote", description="Add a quote to Hlin")
async def add_quote(interaction : discord.Interaction , quote: str):
  toxicity = my_perspective_client.analyze_quote(quote)
  print(toxicity)

  if toxicity < 0.6:
    await interaction.response.send_message(f"{quote} by  {interaction.user.mention} ", ephemeral = True)
    post_quote(quote, str(interaction.user))
  else:
    await interaction.response.send_message(f"Your quote **{quote}** seems inapropriate ", ephemeral = True)
    

@bot.tree.command(name="dayly_quotes", description="Better mornings")
async def test_btn(interaction : discord.Interaction):
  em = My_Button()
  await interaction.response.send_message(content="Activate Dayly Quotes ?", view=em)

bot.run(TOKEN)