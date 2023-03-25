import discord


import os 
from dotenv import load_dotenv
load_dotenv()

"""API KEYS AND TOKENS"""

## Mongo db connection link
MONGO_CONN_LINK =  os.environ['MONGODB_CONN_LINK']
# API URL
API_URL = 'https://zenquotes.io/api/random'
# Google perspective API KEY
PERSPECTIVE_API = os.environ['GOOGLE_PERSPECTIVE_KEY']
# Google Custom Search Json API Key
CUSTOM_SEARCH_API = os.environ["GOOGLE_CUSTOM_SEARCH_KEY"]
SEARCH_ENGINE_ID = os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"]

"""TOXICITY SCRORE"""
TOLERATED_TOXICITY = 0.6


"""BOT INTENTS"""
INTENTS = discord.Intents.default()

