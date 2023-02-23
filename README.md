# Hlin-discord-bot

Share Comfort on Discord 


<div align="center">
  <img width=500px alt='loading' src='https://i.imgur.com/kGSl5r7.png'/>
</div>

## Setup 

### Must have :

 - A bot token from the [discord developer API](https://discord.com/developers/applications)
 - ```python 3.10```
 - A [MongoDB cluster](https://www.mongodb.com/basics/clusters) and/or [MongoDB Shell](https://www.mongodb.com/docs/mongodb-shell/) for testing 
 - A [connection string](https://www.mongodb.com/docs/manual/reference/connection-string/) for your cluster looking like : ```mongodb+srv://<username>:<password>@<cluster-name>mongodb.net/?retryWrites=true&w=majority```
 - A Google Perspective API [key](https://perspectiveapi.com/)
 
### About the Database 

```python
Client_Mongo = MongoClient(MONGO_CONN_LINK)
quotes_db = Client_Mongo.quotes
quotes_collection = quotes_db.quotes_collection
```

By default the a ```quotes``` database is created and the quotes are stored in the ```quotes_collection``` collection.

Note : the quotes are structured like :
```json
{
  "_id":{"$oid":"63f4c572798e1cdb2613fd04"},
  "author":"Walt Whitman","quote":"Simplicity is the glory of expression. ",
  "date":"23:02:21:13:21:54"
}
```

 - *While retrieving a quote from the database a random quote is selected and only ```author``` and ```quote``` fileds are retrieved.*
 
 - *While feeding a quote to the database ```author``` , ```quote``` and a ```date``` fileds are required*. The document to insert looks like : 
 ```python
   doc = {"author":quote_author, "quote":quote_text, "date" : now}
 ```

### Run

 - create an python virtual environment and install the ```requirements.txt```
 - create a ```.env``` file and store your Bot Token , MongoDB connection link and your Perspective API key in following format :
  ```python
    DISCORD_BOT_TOKEN =  "some token"
    MONGODB_CONN_LINK = "some link"
    GOOGLE_PERSPECTIVE_KEY = "some key"
  ```
  - You can use the ```feed_database.py``` file to get quotes from the [zenquotes API](https://zenquotes.io/)(make sure to read the [docs](https://docs.zenquotes.io/zenquotes-documentation/)) or any other(must require further config)
  
 ### Hosting with [replit](https://replit.com/) ? (optional)
 
Replit Servers shut down if 30 minutes pass without them being pinged, so you can work around this by starting a flask server with the ```keep_alive.py``` file and use a website like [Uptime Robot](https://uptimerobot.com/) that will ping your server periodically.

### Bot Stucture

The bot have three commands stored in ```cogs/quote_cogs.py``` :
 - ```inspire``` :  grab a quote from the database  
    - calls the ```utils.get_quote_from_db()``` function
        - returns a ```string``` structured like : ```quote - author```
    - sends the quote string to the user .
    
 - ```add_quote``` : post a quote to the database.
    - calls the ```perspective_client.analyze_quote(quote)``` function 
        - returns a toxicity score 
    - calls the ```utils.post_quote(quote, username)``` function and send the quote to the database based on the toxicity score .
    
 - ```dayly_quotes``` : sends a dayly quote a specified hour 
    - calls the ```utils.setup_dayly_quotes(interation , time)``` function with the provided time in ```HH:MM``` format passed by the user.
        - Update or create if not exist the user's configuration stored in a ```config.js``` file . 
    - The  ```utils.start_scheduled_task()``` function starts on the bot's ```on_ready()``` event
        - reads the configs and triggers the ```utils.send_dayly_quote_to_user(user_id, bot)``` function
        - Sends the quote to the user at the specified  GMT time. 
