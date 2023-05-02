import json
import datetime
import re
import asyncio
import logging
import os 
from dotenv import load_dotenv

import discord 
from discord.ext import commands , tasks
from discord.ext.commands import CommandNotFound
import interactions
from discord import app_commands, Embed
from pymongo import MongoClient
from googleapiclient import discovery
import requests

from utils.scheduled_quote_tasks import start_scheduled_task 
#from utils import send_dayly_quote_to_user, schedule_dayly_quotes, start_scheduled_task,post_quote, load_config_for_user, MyView, ToggleButton , update_dayly_quote_config, my_perspective_client
from keep_alive import keep_alive
from settings import INTENTS

"""SETUP THE BOT"""
load_dotenv()
TOKEN = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix="/", intents = INTENTS)

"""BOT EVENTS"""
@bot.event 
async def on_ready():
    asyncio.create_task(start_scheduled_task(bot=bot))
    logging.info('--------------------Bot Logged IN--------------')
    try:
        synced = await bot.tree.sync()
        logging.info(f"{len(synced)} commands synced")
    except Exception as e :
        logging.error(f"Bot Starting-{e}")
    try :
       await bot.load_extension('cogs.quote_cogs')
    except Exception as e :
       logging.error(f"Loading Cogs-{e}")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
      em = discord.Embed(title=f"Sorry :-( ", description=f"I Don't support this command.", color=ctx.author.color) 
      await ctx.send(embed=em, ephemeral = True, mention_author = True)

""" BOT COMMANDS """
@bot.tree.command(name = "inspire", description="Get a quote")
async def cog_inspire(interaction):
   quote_cog = bot.get_cog('QuoteCog')
   await quote_cog.inspire(interaction)
 
@bot.tree.command(name = "add_quote", description="Add a quote to Hlin")
async def add_quote(interaction : discord.Interaction , quote: str):
   quote_cog = bot.get_cog('QuoteCog')
   await quote_cog.add_quote(interaction, quote) 

@bot.tree.command(name="dayly_quotes", description="Better mornings, takes (hour:minutes) GMT . Ex: '08:10'")
async def setup_dayly_quotes(interaction: discord.Interaction, time_hour: str):
   quote_cog = bot.get_cog('QuoteCog')
   await quote_cog.setup_dayly_quotes(interaction, time_hour)   

@bot.tree.command(name="feelings", description="Happy ,Angry, Sad or Anxious ? Here's a nice article to help with your feelings")
async def feelings(interaction : discord.Interaction, feeling: str):
    quote_cog = bot.get_cog('QuoteCog')
    await quote_cog.feelings(interaction , feeling)

def main():
   #keep it alive for replit 
   #keep_alive()
   logging.basicConfig(filename="botlogs.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)
   logging.getLogger().addHandler(console_handler)
   bot.run(TOKEN)

if __name__ == "__main__":
   main()