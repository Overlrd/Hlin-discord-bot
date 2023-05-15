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
    discord_bot_token : str
    class Config:
        env_file = ".env"


ZENQUOTES_API_URL =' https://zenquotes.io/api/random'
WONDERMIND_ENDPOINT = "https://www.wondermind.com/feelings/"
TOLERATED_TOXICITY = 0.6

INTENTS = discord.Intents.default()
INTENTS.message_content = True

EXTENSIONS_LIST = ["cogs.quote_cogs",]
LOCAL_DB_FILE = Path("db.json")
DAILY_QUOTES_CFG_TABLE = "daily_quotes_config"
BOT_VERSION = 1.1