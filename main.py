import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['TOKEN']
import discord 
import random
# request module to get data from api
import requests
#json to read the api response
import json
from replit import db
intents = discord.Intents.default()
intents.message_content = True


API_URL = 'https://zenquotes.io/api/random'


#keep_alive
from keep_alive import keep_alive


sad_words = ['sad', 'angry','unhappy']

starter_encouragements = [
  'Cheer up',
  'Hang on ',
  'Keep it '
]

if "responding" not in db.keys():
  db['responding'] = True 

def get_quote():
  #make a get request to the zen quotes api
  response = requests.get(API_URL)
  #converting the response to json
  response_json = json.loads(response.text)
  
  #get the message with the key 'q' and the author with  the     key 'a'
  quote = response_json[0]['q'] + " -" + response_json[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]


def  delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements
  







class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
          return


        msg = message.content

        if msg.startswith('!inspire'):
          async with message.channel.typing():
            quote = get_quote()
          await message.reply(quote, mention_author=True)

        if db['responding'] :
          options = starter_encouragements
          if 'encouragements' in db.keys():
            options = options + db['encouragements'].value
        
          if any(word in msg for word in sad_words):
            await message.reply(random.choice(options),  mention_author=True)

        if msg.startswith('!new'):
          encouraging_msg = msg.split('!new ', 1)[1]
          update_encouragements(encouraging_msg)
          await message.reply(f'new quote quote added', mention_author=True)


        if msg.startswith('!del'):
          encouragements = []
          if 'encouragements' in db.keys():
            index = int(msg.split('!del', 1)[1])
            delete_encouragement(index)
            encouragements = db['encouragements']
            await message.reply(f'encouagement removed ')


        if msg.startswith('!list'):
          encouragements = []
          if 'encouragements' in db.keys():
            encouragements = db['encouragements']
          await message.reply(f'List :{encouragements}', mention_author = True)


        if msg.startswith('!responding'):
          value = msg.split('!responding ', 1)[1]
          if value.lower() == "true":
            db['responding'] = True 
            await message.reply('Bot response is on', mention_author = True)
          else:
            db['responding'] = False 
            await message.reply(f'Bot response is off', mention_author = True)
            
        




def main():
  keep_alive()
  client = MyClient(intents=intents)
  client.run(TOKEN)


if __name__ == '__main__':
  main()