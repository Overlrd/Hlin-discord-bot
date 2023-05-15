import asyncio
import datetime
import json
import re
import logging
import os 
import platform
import random

import discord 
from discord.ext.commands import Bot , Context
from discord.ext import commands , tasks
import interactions
from discord import app_commands, Embed
from dotenv import load_dotenv
from pymongo import MongoClient
from googleapiclient import discovery
import requests

from utils.quote_tasks import start_scheduled_task
from keep_alive import keep_alive
from config import Settings , INTENTS , EXTENSIONS_LIST , BOT_VERSION
from cogs.quote_cogs import setup

load_dotenv()
settings = Settings()
bot = Bot(command_prefix="/", intents = INTENTS, application_id = 1050472519217463386)


logging.basicConfig(filename="botlogs.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

async def load_extensions(extensions_list):
    for extension in extensions_list:
        print(extension)
        await bot.load_extension(extension)

@bot.event
async def on_ready():
    asyncio.create_task(start_scheduled_task(bot=bot))
    logging.info(f"Loggged in as {bot.user.name} {BOT_VERSION}")
    logging.info(f"discord.py API version: {discord.__version__}")
    logging.info(f"Python version: {platform.python_version()}")
    logging.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logging.info("-------------------")
    synced = await bot.tree.sync()
    logging.info(f"{len(synced)} commands synced")

@bot.event
async def on_command_error(context: Context, error) -> None:
    embed = discord.Embed(title="Command Not Found", color=discord.Color.blue())
    embed.set_image(url="https://cataas.com/cat/says/don't%20know%20this%20command")
    await context.send(embed=embed)

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        logging.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        logging.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )

if __name__ == "__main__":
   asyncio.run(load_extensions(EXTENSIONS_LIST))
   bot.run(token=settings.discord_bot_token)