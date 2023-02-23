import discord
from discord.ext import commands
from pymongo import MongoClient
import requests
import datetime
import json
import os 
import re 
from utils import perspective_client , MyView, load_config_for_user , get_quote_from_db , get_quote, post_quote
from variables import TOLERATED_TOXICITY

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        print('>>>> QuoteCog Loaded \n')

        """ SETUP CONNECTION WITH MONGODB """

        """GOOGLE PERSCEPCTIVE """
        PERSPECTIVE_API = os.environ['GOOGLE_PERSPECTIVE_KEY']
        self.my_perspective_client = perspective_client(PERSPECTIVE_API)

        """BOT"""
        self.bot = bot 

    @commands.command(name = "inspire", description="Get a quote")
    async def inspire(self, ctx):
        #quote = get_quote()
        quote = get_quote_from_db()
        try :
            await ctx.response.send_message(quote)
            print(f">>>> New quote sended to {ctx.user} \n")
        except discord.errors.HTTPException :
            pass


    @commands.command(name = "add_quote", description="Add a quote to Hlin")
    async def add_quote(self , interaction , quote: str):
        toxicity = self.my_perspective_client.analyze_quote(quote)
        print(f">>>> {quote} => {toxicity} \n")

        if toxicity < TOLERATED_TOXICITY:
            await post_quote(quote, str(interaction.user))
            try :
                await interaction.response.send_message(f"{quote} by  {interaction.user.mention}")
            except discord.errors.HTTPException:
                pass
        else:
            try :
                await interaction.response.send_message(f"Your quote **{quote}** seems inapropriate ", ephemeral=True)
            except  discord.errors.HTTPException:
                pass

    @commands.command(name="dayly_quotes", description="")
    async def setup_dayly_quotes(self , interaction , time_hour: str):
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
        await interaction.response.send_message(content=f"Activate Dayly Quotes at {time_hour} GMT ?", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(QuoteCog(bot))






    


