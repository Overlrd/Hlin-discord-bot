import json
import asyncio 

from tqdm import tqdm
import aiohttp

from utils.quote_utils import Quote ,  quotes_collection , post_quote

message = "FEED_DATABASE - MAKE SURE TO CHECK THE README"
attribution = 'Inspirational quotes provided by Zen Quote API-"{}"'.format("https://github.com/magnus-leksell/zen-quote")
API_URL = "https://leksell.io/zen//api/quotes/random"

print(message)
print(attribution)

N = int(input(f"NUMBER OF QUOTES TO PUSH TO DATABASE : "))

async def fetch_quote(session, url):
    async with session.get(url) as response:
        return await response.json()
    
async def main(number_of_quotes):
    async with aiohttp.ClientSession() as session:
        quote_list = []
        for i in tqdm(range(number_of_quotes)):
            response_json = await fetch_quote(session, API_URL)
            quote = Quote(response_json['author'],response_json['quote'])
            quote_list.append(quote)

            if (len(quote_list)) % (number_of_quotes/4) == 0:
                window = -number_of_quotes/4
                post_quote(*quote_list[window:])
                print(f"ADDED {len(quote_list)} QUOTES TO DB")
if __name__ == '__main__':
    asyncio.run(main(number_of_quotes=N))