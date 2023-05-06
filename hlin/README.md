# Hlin-discord-bot [<img height="50" align="right" src="https://user-images.githubusercontent.com/90383672/227210489-8d09a2f7-2eeb-460d-8c02-aef93fa5a4a3.png">](https://discord.com/api/oauth2/authorize?client_id=1050472519217463386&permissions=2048&scope=bot)

A discord bot to generate inspiring and comforting quotes , part of the [Hlin project](https://overlrd.github.io/hlin/) 






<br>

<div align="center">
  <img width=500px alt='loading' src='https://i.imgur.com/kGSl5r7.png'/>
</div>

# Setup

## Prerequisites

To run the bot, you will need the following:

 - A bot token from the [discord developer API](https://discord.com/developers/docs/topics/oauth2)
 - [Python 3.10](https://www.python.org/downloads/release/python-3100/) installed on your system
 - A [MongoDB cluster](https://cloud.mongodb.com/v2#/clusters) and/or [MongoDB Shell]() for testing
 - A connection string for your cluster in the format :
   -  "mongodb+srv:// ```username``` : ```password``` @ ```cluster-name``` mongodb.net/?retryWrites=true&w=majority"
 
 - A [Google Perspective API key](https://developers.perspectiveapi.com/s/docs-get-started?language=en_US)
  
**Helpfull Ressources**
 - [Python MongoDB Tutorial using PyMongo](https://www.youtube.com/watch?v=rE_bJl2GAY8)
 - [How to get your discord bot token](https://www.youtube.com/watch?v=aI4OmIbkJH8)

 ## Running the Bot
To run the bot:

 - Create a Python virtual environment and install the dependencies listed in requirements.txt
 ```shell
  $ python3 -m venv .virtual-env
  $ source .virtual-env/bin/activate
  $ pip install -r requirements.txt
  ```

 - Run the ```setup.py``` file to automaticaly create and write ```config.json``` and ```.env``` files
 ```shell
  $ python3 setup.py
 
 ```
 - You will need to provide your ```Discord Bot token``` , ```Mongodb Connection Link``` and ```Google Perspective API Key``` 

  
 - Run the ```feed_database.py``` file to get quotes from the [zenquotes](https://zenquotes.io/) API (make sure to read the [docs](https://docs.zenquotes.io/zenquotes-documentation/)) or any other API (which may require further configuration).
 ```shell
 $ python3 feed_database.py
 
 ```
 
 - And start the Bot 
 ```shell
 $ python3 main.py
 
 ```

### Hosting with Replit (optional)
If you plan to host the bot with replit.com, note that the Replit servers shut down if 30 minutes pass without them being pinged. To work around this, you can start a Flask server with the ```keep_alive.py``` file and use a website like [Uptime Robot](https://uptimerobot.com/) that will ping your server periodically.
  
  


### About the Database
By default, a database called ```quotes``` will be created, and the quotes will be stored in a collection called ```quotes_collection```.

The quotes are structured as follows:

```json
{
  "_id": { "$oid": "63f4c572798e1cdb2613fd04" },
  "author": "Walt Whitman",
  "quote": "Simplicity is the glory of expression. ",
  "date": "23:02:21:13:21:54"
}
```
  
  
When retrieving a quote from the database, a random quote is selected, and only the ```author``` and quote ```fields``` are retrieved.

When feeding a quote to the database, the ```author, ```quote```, and ```date``` fields are required. The document to insert should look like:

```python
doc = { "author": quote_author, "quote": quote_text, "date": now }
```
  

## Bot Structure

The bot has three commands stored in `cogs/quote_cogs.py`:

- `inspire`: grab a quote from the database.
  - Calls the `utils.get_quote_from_db()` function.
  - Returns a `string` structured like: `quote - author`.
  - Sends the quote string to the user.

- `add_quote`: post a quote to the database.
  - Calls the `perspective_client.analyze_quote(quote)` function.
  - Returns a toxicity score.
  - Calls the `utils.post_quote(quote, username)` function and sends the quote to the database based on the toxicity score.

- `daily_quotes`: sends a daily quote at a specified hour.
  - Calls the `utils.setup_daily_quotes(interaction, time)` function with the provided time in `HH:MM` format passed by the user.
  - Updates or creates if not exist the user's configuration stored in a `config.json` file.
  - The `utils.start_scheduled_task()` function starts on the bot's `on_ready()` event.
  - Reads the configs and triggers the `utils.send_daily_quote_to_user(user_id, bot)` function.
  - Sends the quote to the user at the specified GMT time.

