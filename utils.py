import os 
import json 
import requests
import datetime
from pymongo import MongoClient
from googleapiclient import discovery
import discord
import asyncio
from dotenv import load_dotenv
load_dotenv()


""" VARIABLES """
from variables import MONGO_CONN_LINK, API_URL , PERSPECTIVE_API



""" SETUP DATABASE"""
Client_Mongo = MongoClient(MONGO_CONN_LINK)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection


""" UTILITY FUNCTIONS """
## Get quote from API

def get_quote():
  #make a get request to the zen quotes api
  response = requests.get(API_URL)
  #converting the response to json
  response_json = json.loads(response.text)
  
  #get the message with the key 'q' and the author with  the     key 'a'
  quote = response_json[0]['q'] + " -" + response_json[0]['a']
  return quote

## Get quote from Mongo db
def get_quote_from_db():
    #get random q
    random = quotes_collection.aggregate([{ "$sample": { "size": 1 } }])
    for i in random:
      quote = f"{i['quote']} - {i['author']}"
    return quote


async def post_quote(quote_text, quote_author):
  now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
  #quote_author = quote_author.split("@", 1)[1]
  doc = {"author":quote_author, "quote":quote_text, "date" : now}
  try :
    quotes_collection.insert_one(doc)
    print(">>>> new quote sended to db \n")
  except Exception as e:
    print(e)

def load_config_for_user(user_id="all", file_path="config.json"):
    with open(file_path, "r") as file:
        data = json.load(file)
        dayly_config = data.get('dayly_quotes_config', {})

        if user_id == "all":
            # Return a dictionary of user IDs and configurations
            return {user_id: json.loads(config) if isinstance(config, str) else config for user_id, config in dayly_config.items()}
        else:
            return dayly_config.get(str(user_id), {})



## update or create config for dayly quote
def update_dayly_quote_config(user_id, set_dayly, when="none", file_path="config.json"):
    doc = {str(user_id): {"dayly": str(set_dayly), "when": str(when)}}

    with open(file_path, "r") as file:
        data = json.load(file)
        dayly_config = data['dayly_quotes_config']
        dayly_config.update(doc)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    if set_dayly:
        message = f"Daily quotes have been activated for {when}."
    else:
        message = "Daily quotes have been deactivated."
        
    return message


async def send_dayly_quote_to_user(User_id, bot ):
   user = await bot.fetch_user(User_id)
   message =  get_quote_from_db()
   print(f">>>> sending new message to {user} \n")
   await user.send(message)

async def schedule_dayly_quotes(users_configs,bot):
    now =  datetime.datetime.now().strftime('%H:%M')
    print(f">>>> Task Restarted at : {now} \n")
    print(f">>>> Reading {len(users_configs)} user's config ...\n")
    for user_id , config in users_configs.items():
        if config['dayly'] == "1" and now == config['when']:
            print(f">>>> {config['when']} => should send message" )
            await send_dayly_quote_to_user(User_id=user_id, bot=bot)

async def start_scheduled_task(bot):
    while True:
        print(">>>> started start_scheduled_task function \n")
        users_configs = load_config_for_user("all")
        await schedule_dayly_quotes(users_configs,bot=bot)
        await asyncio.sleep(60)



""" UTILITY CLASSES """
class perspective_client():
  def __init__(self, key):
    self.pers_client = discovery.build(
          "commentanalyzer",
          "v1alpha1",
          developerKey=key,
          discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
          static_discovery=False,
        )
  def analyze_quote(self, text_to_analyze):
    analyze_request = {
      'comment': { 'text':  text_to_analyze},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = self.pers_client.comments().analyze(body=analyze_request).execute()
    response = json.dumps(response, indent=2)
    response_to_dict = json.loads(response)
    toxicity = response_to_dict['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity
  
my_perspective_client = perspective_client(PERSPECTIVE_API)


class ToggleButton(discord.ui.Button):
    def __init__(self, active, **kwargs):
        self.active = active
        label = "Deactivate" if active else "Activate"
        super().__init__(label=label, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.active = not self.active

        current_state = "Activated" if self.active else "Deactivated"
        label = "Deactivate" if self.active else "Activate"
        self.label = label
        await interaction.response.edit_message(content=f"Moring Quotes. {current_state} ", view=self.view)
        update_dayly_quote_config(interaction.user.id, int(self.active), when=self.view.when)


class MyView(discord.ui.View):
    def __init__(self, when, active):
        self.when = when
        super().__init__(timeout=None)
        self.add_item(ToggleButton(active))
