import json
import datetime
import re
import asyncio
import logging
import os 
from dotenv import load_dotenv

import discord 
from discord.ext import commands
import interactions
from discord import app_commands, Embed
from pymongo import MongoClient
from googleapiclient import discovery
import requests

from hlin.utils.quote_tasks import start_scheduled_task 
from keep_alive import keep_alive
from hlin.config import Settings , INTENTS , EXTENTIONS_LIST

load_dotenv()
settings = Settings()
bot = commands.Bot(command_prefix="/", intents = INTENTS)

def main():
   logging.basicConfig(filename="botlogs.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)
   logging.getLogger().addHandler(console_handler)

   for extention in EXTENTIONS_LIST:
      bot.load_extension(extention)

if __name__ == "__main__":
   main()

@bot.event 
async def on_ready():
    asyncio.create_task(start_scheduled_task(bot=bot))
    logging.info(f"{bot.user.name} logged in with discord version {discord.__version__}")
    synced = await bot.tree.sync()
    logging.info(f"{len(synced)} commands synced")

bot.run(token=settings.discord_bot_token)