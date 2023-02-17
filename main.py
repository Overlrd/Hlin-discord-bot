import discord 
from discord.ext import commands , tasks
from discord.ext.commands import CommandNotFound
import interactions
from googleapiclient import discovery
import os 
import requests
import json
from discord import app_commands, Embed
from pymongo import MongoClient
from datetime import datetime
import re

# e load env variables
from dotenv import load_dotenv
load_dotenv()
from utils import load_config_for_user, MyView, ToggleButton, quotes_collection , get_quote_from_db , post_quote, update_dayly_quote_config, my_perspective_client, My_Button

## set up the bot 
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())


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
  print(f"{toxicity} for {quote}")

  if toxicity < 0.6:
    post_quote(quote, str(interaction.user))
    await interaction.response.send_message(f"{quote} by  {interaction.user.mention} ", ephemeral = True)

  else:
    await interaction.response.send_message(f"Your quote **{quote}** seems inapropriate ", ephemeral = True)
    #print("message is toxic ") 

@bot.tree.command(name="dayly_quotes", description="Better mornings, takes (hour:minutes). Ex: '08:10'")
async def test_btn(interaction: discord.Interaction, time_hour: str):
    # Check that the time_hour string is in the correct format (HH:MM)
    if not re.match(r"^\d{2}:\d{2}$", time_hour):
        await interaction.response.send_message(
            content="Invalid time format. Please enter a time in the format HH:MM.",
            ephemeral=True,
            delete_after=10,
        )
        return

    # Check if the user has already activated dayly quotes
    user_config = load_config_for_user(interaction.user.id)
    active = user_config.get("dayly_quotes_config", {}).get(str(interaction.user.id), {}).get("dayly", 0)

    view = MyView(when=time_hour, active=active)
    await interaction.response.send_message(content=f"Activate Dayly Quotes at {time_hour}?", view=view, ephemeral=True)

bot.run(TOKEN)