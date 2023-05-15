import logging
import asyncio
import datetime

import discord

from utils.quote_utils import get_quote_from_db
from utils.storage import UserConfig
from config import Settings , DAILY_QUOTES_CFG_TABLE , LOCAL_DB_FILE

settings = Settings()
cfg = UserConfig(LOCAL_DB_FILE)

async def send_dayly_quote_to_user(User_id, bot ):
   user = await bot.fetch_user(User_id)
   message =  get_quote_from_db()
   logging.info(f"sending new message to {user}")
   await user.send(message)

async def schedule_dayly_quotes(bot):
    now =  datetime.datetime.now().strftime('%H:%M')
    logging.info(f"Task Restarted at : {now}")
    cfgs = cfg.search_config(daily = True , when = now)
    logging.info(f"Reading {len(cfgs)} user's config")
    for user in cfgs:
            await send_dayly_quote_to_user(User_id=user['discord_id'], bot=bot)

async def start_scheduled_task(bot):
    while True:
        logging.info(f"started start_scheduled_task function")
        await schedule_dayly_quotes(bot=bot)
        await asyncio.sleep(60)
