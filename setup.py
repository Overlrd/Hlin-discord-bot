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


# Create the .env file and write the variables to it
def create_env_and_vars():
    try :
        DISCORD_BOT_TOKEN = input("YOUR DISCORD API KEY : ")
        MONGODB_CONN_LINK = input("YOUR MONGODB CONN LINK : ")
        GOOGLE_PERSPECTIVE_KEY = input("YOUR GOOGLE PERSPECTIVE API KEY : ")
        GOOGLE_CUSTOM_SEARCH_KEY = input("YOUR GOOGLE CUSTOM SEARCH KEY : ")
        GOOGLE_CUSTOM_SEARCH_ENGINE_ID = input("YOUR CUSTOM SEARCH ENGINE ID KEY : ")
    except EOFError :
        return
        
    logging.info("writing env variables")
    with open(".env", "w") as file:
        file.write(f'DISCORD_BOT_TOKEN= "{DISCORD_BOT_TOKEN}"\n')
        file.write(f'MONGODB_CONN_LINK= "{MONGODB_CONN_LINK}"\n')
        file.write(f'GOOGLE_PERSPECTIVE_KEY= "{GOOGLE_PERSPECTIVE_KEY}"\n')
        file.write(f'GOOGLE_CUSTOM_SEARCH_KEY= "{GOOGLE_CUSTOM_SEARCH_KEY}"\n')
        file.write(f'GOOGLE_CUSTOM_SEARCH_ENGINE_ID= "{GOOGLE_CUSTOM_SEARCH_ENGINE_ID}"\n')

def create_config_file(config_file_name="config.json"):
    logging.info(f"writing config file at {config_file_name}")
    config_data = {
        "dayly_quotes_config": {}
    }

    with open(config_file_name, "w") as f:
        json.dump(config_data, f, indent=4)

try :
    create_env_and_vars()
    create_config_file()
    print(f"{Fore.GREEN} SETUP COMPLETED - RUN 'python3 main.py' TO START THE BOT {Style.RESET_ALL}")
except Exception as e :
    print(f"{e}")