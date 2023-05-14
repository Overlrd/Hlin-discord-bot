import os 
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import discord
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Pydantic BaseSettings instance loading some settings('lowercase one's') from ".env" file. \n
    `mongodb_conn_link` : Mongodb connection link \n
    `google_perspective_key` : Google Perspective api key \n
    `google_custom_search_key` : Google custom search API key \n
    `google_custom_search_engine_id` : you know
    """
    mongodb_conn_link : str 
    google_perspective_key : str
    google_custom_search_key : str
    google_custom_search_engine_id : str

    ZENQUOTES_API_URL =' https://zenquotes.io/api/random'
    WONDERMIND_ENDPOINT = "https://www.wondermind.com/article/"
    TOLERATED_TOXICITY = 0.6
    INTENTS = discord.Intents.default()

    class Config:
        env_file = ".env"


"""API KEYS AND TOKENS"""
## Mongo db connection link
MONGO_CONN_LINK =  os.environ['MONGODB_CONN_LINK']
# Zenquotes API URL
API_URL = 'https://zenquotes.io/api/random'
# Google perspective API KEY
PERSPECTIVE_API = os.environ['GOOGLE_PERSPECTIVE_KEY']
# Google Custom Search Json API Key
CUSTOM_SEARCH_API = os.environ["GOOGLE_CUSTOM_SEARCH_KEY"]
SEARCH_ENGINE_ID = os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"]
# Wondermind URL 
CUSTOM_SEARCH_WONDERMIND_URL = "https://www.wondermind.com/article/"
#TOLERATED TOXICITY
TOLERATED_TOXICITY = 0.6
#BOT INTENTS
INTENTS = discord.Intents.default()
#CONFIG FILE PATH
CONFIG_FILE_PATH = Path("config.json")
DEFAULT_CONFIG = "dayly_quotes_config"