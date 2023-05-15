import os
import json 
import logging

message = "--------------SETUP - MAKE SURE TO CHECK THE README-------------------"
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
    with open("./hlin/.env", "w") as file:
        try :
            file.write(f'DISCORD_BOT_TOKEN= "{DISCORD_BOT_TOKEN}"\n')
            file.write(f'MONGODB_CONN_LINK= "{MONGODB_CONN_LINK}"\n')
            file.write(f'GOOGLE_PERSPECTIVE_KEY= "{GOOGLE_PERSPECTIVE_KEY}"\n')
            file.write(f'GOOGLE_CUSTOM_SEARCH_KEY= "{GOOGLE_CUSTOM_SEARCH_KEY}"\n')
            file.write(f'GOOGLE_CUSTOM_SEARCH_ENGINE_ID= "{GOOGLE_CUSTOM_SEARCH_ENGINE_ID}"\n')
        except Exception as e :
            logging.exception(e)
        else :
            print("SETUP COMPLETED - EXECUTE 'main.py' TO CONTINUE ")
        


if __name__ == "__main__":
    create_env_and_vars()
