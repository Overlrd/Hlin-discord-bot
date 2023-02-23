import discord 
from discord.ext import commands , tasks
from discord.ext.commands import CommandNotFound
import interactions
from discord import app_commands, Embed

from pymongo import MongoClient
from googleapiclient import discovery

import os 
import requests
import json
import datetime
import re
import asyncio

from dotenv import load_dotenv
load_dotenv()

from utils import send_dayly_quote_to_user, schedule_dayly_quotes, start_scheduled_task,post_quote, load_config_for_user, MyView, ToggleButton , update_dayly_quote_config, my_perspective_client
from keep_alive import keep_alive

"""SETUP THE BOT"""
TOKEN = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())

"""BOT EVENTS"""
@bot.event 
async def on_ready():
    asyncio.create_task(start_scheduled_task(bot=bot))

    print(f'--------------------Logged--------------')

    try:
        synced = await bot.tree.sync()
        print(f">>>> {len(synced)} commands synced \n" )
    except Exception as e :
        print(f">>>> {e} \n")

    try :
       await bot.load_extension('cogs.quote_cogs')
    except Exception as e :
       print(f">>>> {e} \n")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
      em = discord.Embed(title=f"Sorry :-( ", description=f"I Don't support this command.", color=ctx.author.color) 
      await ctx.send(embed=em, ephemeral = True, mention_author = True)


""" BOT COMMANDS """
@bot.tree.command(name = "inspire", description="Get a quote")
async def cog_inspire(interaction):
   quote_cog = bot.get_cog('QuoteCog')
   print('>>>> QuoteCog.Inspire \n')
   await quote_cog.inspire(interaction)    
 
@bot.tree.command(name = "add_quote", description="Add a quote to Hlin")
async def add_quote(interaction : discord.Interaction , quote: str):
   quote_cog = bot.get_cog('QuoteCog')
   print('>>>> QuoteCog.add_post \n')
   await quote_cog.add_quote(interaction, quote) 

@bot.tree.command(name="dayly_quotes", description="Better mornings, takes (hour:minutes) GMT . Ex: '08:10'")
async def setup_dayly_quotes(interaction: discord.Interaction, time_hour: str):
   quote_cog = bot.get_cog('QuoteCog')
   print('>>>> QuoteCog.setup_dayly_quotes \n')
   await quote_cog.setup_dayly_quotes(interaction, time_hour)   

def main():
   #keep it alive whle using replit 
   #keep_alive()
   bot.run(TOKEN)

if __name__ == "main":
   main()
