import os 
import json 
import requests
import datetime
from pymongo import MongoClient
from googleapiclient import discovery
import discord
from discord.ui import Select, View
import pytz
from dotenv import load_dotenv
load_dotenv()


""" VARIABLES """
## Mongo db connection link
MONGO_CONN_LINK =  os.environ['CONN_LINK']
# API URL
API_URL = 'https://zenquotes.io/api/random'
# Google perspective API KEY
PERSPECTIVE_API = os.environ['G_PER_TOKEN']


""" SETUP DATABASE"""
Client_Mongo = MongoClient(MONGO_CONN_LINK)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection


""" UTILITARY FUNCTIONS """
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


""" UTILITARY CLASSES """
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


class My_Button(discord.ui.View):
    def __init__(self, when):
        self.when = when
        super().__init__()
        
    @discord.ui.button(label="Activate", style= discord.ButtonStyle.primary)
    async def activate(self, interaction: discord.Interaction, button: discord.ui.Button):
        print('should update config here ')

        message = await update_dayly_quote_config(interaction.user.id, 1, when=self.when)

        await print("should send message here ")
        await interaction.response.send_message(message, ephemeral=True)

    @discord.ui.button(label="Deactivate", style= discord.ButtonStyle.danger)
    async def deactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        print('should update config here ')
        message = await update_dayly_quote_config(interaction.user.id, 0)
        await print('should send message here ')
        await interaction.response.send_message(message, ephemeral=True)


def load_config_for_user(user_id="all", file_path="config.json"):
    with open(file_path, "r") as file:
        data = json.load(file)
        dayly_config = data.get('dayly_quotes_config', {})

        if user_id == "all":
            # Return a dictionary of user IDs and configurations
            return {user_id: json.loads(config) if isinstance(config, str) else config for user_id, config in dayly_config.items()}
        else:
            return dayly_config.get(str(user_id), {})



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

my_perspective_client = perspective_client(PERSPECTIVE_API)


#### 
class TimezoneSelect(View):
    @discord.ui.select(
      placeholder="select something ..",
      options=[
        discord.SelectOption(label="Option 1" , value="1"),
        discord.SelectOption(label="Option 2" , value="2"),
        discord.SelectOption(label="Option 3" , value="3")
      ]
    )

    async def callback(self, select , interaction):
        print(interaction)
        selected_tz = pytz.timezone(interaction.values[0])
        print('exec callback'+  interaction.message.components[0])
        await interaction.response.send_message(f'The current time in {selected_tz.zone} is {datetime.datetime.now(selected_tz).strftime("%Y-%m-%d %H:%M:%S")}.')


