import os
import json 
import logging
from dotenv import load_dotenv

from colorama import init, Fore, Style

init()
load_dotenv()

message = "--------------SETUP - MAKE SURE TO CHECK THE README-------------------"
print(f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")

# Define the variables to be written to the .env file
DISCORD_BOT_TOKEN = str(input(f"{Fore.GREEN} YOUR DISCORD API KEY : {Style.RESET_ALL}"))
MONGODB_CONN_LINK = str(input(f"{Fore.GREEN} YOUR MONGODB CONN LINK : {Style.RESET_ALL}"))
GOOGLE_PERSPECTIVE_KEY = str(input(f"{Fore.GREEN} YOUR GOOGLE PERSPECTIVE API KEY : {Style.RESET_ALL}"))

# Create the .env file and write the variables to it
def create_env_and_vars(discord_bot_token , mongodb_conn_link , google_perspective_key):
    logging.info("writing env variables")
    with open(".env", "w") as file:
        file.write(f'DISCORD_BOT_TOKEN= "{discord_bot_token}"\n')
        file.write(f'MONGODB_CONN_LINK= "{mongodb_conn_link}"\n')
        file.write(f'GOOGLE_PERSPECTIVE_KEY= "{google_perspective_key}"\n')


def create_config_file(config_file_name="config.json"):
    logging.info(f"writing config file at {config_file_name}")
    config_data = {
        "dayly_quotes_config": {}
    }

    with open(config_file_name, "w") as f:
        json.dump(config_data, f, indent=4)

try :
    create_env_and_vars(DISCORD_BOT_TOKEN, MONGODB_CONN_LINK, GOOGLE_PERSPECTIVE_KEY)
    create_config_file()
    print(f"{Fore.GREEN} SETUP COMPLETED - RUN 'python3 main.py' TO START THE BOT {Style.RESET_ALL}")
except Exception as e :
    print(f"{Fore.RED} {e} {Style.RESET_ALL}")

