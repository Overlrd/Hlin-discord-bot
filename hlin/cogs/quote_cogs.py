import asyncio
import datetime
import json
import os 
import re 
import logging

import discord
from discord.ext import commands
from pymongo import MongoClient
import requests

from config import Settings , LOCAL_DB_FILE , DAILY_QUOTES_CFG_TABLE , TOLERATED_TOXICITY
from utils.quote_utils import Quote , get_quote_from_db , post_quote
from utils.perspective import perspective_client
from utils.views import ToggleButton , MyView , Dropdown
from utils.storage import UserConfig
from utils.wondermind import search_by_feelings

settings = Settings()
cfg = UserConfig(LOCAL_DB_FILE)

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        logging.info("QuoteCog Loaded")
        self.my_perspective_client = perspective_client(settings.google_perspective_key)
        """BOT"""
        self.bot = bot 

    @commands.hybrid_command(name = "inspire", description="Get a quote")
    async def inspire(self, ctx):
        #quote = get_quote()
        logging.info("Called QuoteCog.inspire")
        quote = get_quote_from_db()
        try :
            await ctx.send(quote)
            logging.info(f"New quote sended to {ctx.author}")
        except discord.errors.HTTPException :
            pass


    @commands.hybrid_command(name = "add_quote", description="Add a quote to Hlin")
    async def add_quote(self , ctx , quote: str):
        logging.info("Called QuoteCog.add_quote")

        toxicity = self.my_perspective_client.analyze_quote(quote)
        logging.info(f"{quote} => {toxicity}")
        NewQuote = Quote(ctx.author.name,quote)
        if toxicity < TOLERATED_TOXICITY:
            post_quote(NewQuote)
            try :
                await ctx.send(f"{quote} by  {ctx.author.mention}")
            except discord.errors.HTTPException as e:
                logging.warning(f"{e}")
        else:
            try :
                await ctx.send(f"Your quote **{quote}** seems inapropriate ")
            except  discord.errors.HTTPException as e:
                logging.warning(f"{e}")

    @commands.hybrid_command(name="dayly-quotes", description="")
    async def setup_dayly_quotes(self, ctx, time_hour: str):
        logging.info("Called QuoteCog.dayly_quotes")
        # Check that the time_hour string is in the correct format (HH:MM)
        if not re.match(r"^\d{2}:\d{2}$", time_hour):
            await ctx.send(
                content="Invalid time format. Please enter a time in the format HH:MM.",
                delete_after=10,
            )
            return
        # Check if the user has already activated daily quotes
        user_config = cfg.read_config(ctx.author.id)
        active = user_config.get("daily", 0)
        view = MyView(ctx=ctx, when=time_hour, active=active)
        await ctx.send(content=f"Activate Daily Quotes at {time_hour} GMT ?", view=view, delete_after=None)

    @commands.hybrid_command(name="filter-by-feels", description = "How Are You Feeling?")
    async def feelingstest(self, ctx):
        await ctx.send("How do you feel ?", view = Dropdown())


async def setup(bot):
    await bot.add_cog(QuoteCog(bot))
