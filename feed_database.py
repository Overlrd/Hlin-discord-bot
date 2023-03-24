from utils import quotes_collection
import datetime
import time
import logging
from tqdm import tqdm
import asyncio 
import aiohttp
import json


from colorama import init, Fore, Style
init()
message = "--------------FEED_DATABASE - MAKE SURE TO CHECK THE README-------------------"
attribution = 'Inspirational quotes provided by Zen Quote API-"https://github.com/magnus-leksell/zen-quote"'
print(f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")
print(f"{Fore.RED}{Style.BRIGHT}{attribution}{Style.RESET_ALL}")

N = int(input(f"{Fore.GREEN} NUMBER OF QUOTES TO PUSH TO DATABASE : {Style.RESET_ALL}"))


API_URL = "https://leksell.io/zen//api/quotes/random"


async def fetch_quote(session, url):
    async with session.get(url) as response:
        return await response.json()
    
def post_quote(quote_text, quote_author, last_posted_index):
    now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
    many_docs = []
    for i in range(last_posted_index + 1, len(quote_text)):
        doc = {"author": quote_author[i], "quote": quote_text[i], "date": now}
        many_docs.append(doc)
    try:
        quotes_collection.insert_many(many_docs)
        logging.info(f"{len(many_docs) + last_posted_index} sended to db")
        return len(many_docs)
    except Exception as e:
        print(e)
        logging.error(e)
        return 0

async def main(number_of_quotes):
    async with aiohttp.ClientSession() as session:
        quote_list = []
        author_list = []
        last_posted_index = -1
        for i in tqdm(range(number_of_quotes)):
            response_json = await fetch_quote(session, API_URL)
            quote_list.append(response_json['quote'])
            author_list.append(response_json['author'])
            if (len(quote_list)) % (number_of_quotes/4) == 0:
                num_sent = post_quote(quote_text=quote_list, quote_author=author_list, last_posted_index=last_posted_index)
                last_posted_index += num_sent
        print(f"{Fore.GREEN}{Style.BRIGHT}-------------{last_posted_index + 1} QUOTES SUCCESSFULLY SENDED TO DATABASE --------------{Style.RESET_ALL}")


if __name__ == '__main__':
    asyncio.run(main(number_of_quotes=N))