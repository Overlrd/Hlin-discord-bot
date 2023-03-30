import logging
import asyncio
import datetime

import discord

from utils.quotes_action import get_quote_from_db
from utils.config_actions import load_config_for_user

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
        if config['dayly'] == "1" and now == config['when']:
            logging.info(f"{config['when']} => should send message")
            await send_dayly_quote_to_user(User_id=user_id, bot=bot)

async def start_scheduled_task(bot):
    while True:
        logging.info(f"started start_scheduled_task function")
        users_configs = load_config_for_user("all")
        await schedule_dayly_quotes(users_configs,bot=bot)
        await asyncio.sleep(60)
