import logging
import asyncio
import datetime

import discord

from hlin.utils.quote_utils import get_quote_from_db
from hlin.utils.storage import UserConfig
from hlin.config import Settings , DAILY_QUOTES_CFG_TABLE , LOCAL_DB_FILE

settings = Settings()
cfg = UserConfig(LOCAL_DB_FILE)

async def send_dayly_quote_to_user(User_id, bot ):
   user = await bot.fetch_user(User_id)
   message =  get_quote_from_db()
   logging.info(f"sending new message to {user}")
   await user.send(message)

async def schedule_dayly_quotes(users_configs,bot):
    now =  datetime.datetime.now().strftime('%H:%M')
    logging.info(f"Task Restarted at : {now}")
    logging.info(f"Reading {len(users_configs)} user's config")
    for user_id , config in users_configs.items():
        if config['daily'] == True and now == config['when']:
            logging.info(f"{config['when']} => should send message")
            await send_dayly_quote_to_user(User_id=user_id, bot=bot)

async def start_scheduled_task(bot):
    while True:
        logging.info(f"started start_scheduled_task function")
        users_configs = cfg.read_config("all")
        await schedule_dayly_quotes(users_configs,bot=bot)
        await asyncio.sleep(60)
