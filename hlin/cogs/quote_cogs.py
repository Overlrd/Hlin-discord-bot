import datetime
import json
import os 
import re 
import logging

import discord
from discord.ext import commands
from pymongo import MongoClient
import requests

from hlin.config import Settings , LOCAL_DB_FILE , DAILY_QUOTES_CFG_TABLE , TOLERATED_TOXICITY
from utils.quote_utils import Quote , get_quote_from_db , post_quote
from hlin.utils.perspective import perspective_client
from hlin.utils.views import ToggleButton , MyView
from hlin.utils.storage import UserConfig
from utils.wondermind import search_by_feelings

settings = Settings()
cfg = UserConfig(LOCAL_DB_FILE)

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        logging.info("QuoteCog Loaded")
        self.my_perspective_client = perspective_client(settings.google_perspective_key)
        """BOT"""
        self.bot = bot 

    @commands.command(name = "inspire", description="Get a quote")
    async def inspire(self, ctx):
        #quote = get_quote()
        logging.info("Called QuoteCog.inspire")
        quote = get_quote_from_db()
        try :
            await ctx.response.send_message(quote)
            logging.info(f"New quote sended to {ctx.user}")
        except discord.errors.HTTPException :
            pass


    @commands.command(name = "add_quote", description="Add a quote to Hlin")
    async def add_quote(self , interaction , quote: str):
        logging.info("Called QuoteCog.add_quote")

        toxicity = self.my_perspective_client.analyze_quote(quote)
        logging.info(f"{quote} => {toxicity}")
        NewQuote = Quote(interaction.user,quote)
        if toxicity < TOLERATED_TOXICITY:
            post_quote(NewQuote)
            try :
                await interaction.response.send_message(f"{quote} by  {interaction.user.mention}")
            except discord.errors.HTTPException as e:
                logging.warning(f"{e}")
        else:
            try :
                await interaction.response.send_message(f"Your quote **{quote}** seems inapropriate ", ephemeral=True)
            except  discord.errors.HTTPException as e:
                logging.warning(f"{e}")

    @commands.command(name="dayly_quotes", description="")
    async def setup_dayly_quotes(self , interaction , time_hour: str):
        logging.info("Called QuoteCog.dayly_quotes")
        # Check that the time_hour string is in the correct format (HH:MM)
        if not re.match(r"^\d{2}:\d{2}$", time_hour):
            await interaction.response.send_message(
                content="Invalid time format. Please enter a time in the format HH:MM.",
                ephemeral=True,
                delete_after=10,
            )
            return
        # Check if the user has already activated dayly quotes
        logging.info("QuoteCog.dayly_quotes - reading user config ")
        user_config = cfg.read_config(interaction.user.id)
        active = user_config.get("daily", 0)
        logging.info("QuoteCog.dayly_quotes - updating view ")
        view = MyView(when=time_hour, active=active)
        await interaction.response.send_message(content=f"Activate Dayly Quotes at {time_hour} GMT ?", view=view, ephemeral=True)

    @commands.command(name="feeling")
    async def feelings(self, interaction , feeling : str):
        logging.info("called quotecog.feelings")
        item = search_by_feelings(q=feeling,key=settings.google_custom_search_key, cx=settings.google_custom_search_engine_id)
        await interaction.response.send_message(content=f"{item['link']}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(QuoteCog(bot))
