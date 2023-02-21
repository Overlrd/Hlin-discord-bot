from utils import get_quote, quotes_collection
import datetime
import time
def post_quote(quote_text, quote_author, last_posted_index):
    now = datetime.datetime.now().strftime("%y:%m:%d:%H:%M:%S")
    many_docs = []
    for i in range(last_posted_index + 1, len(quote_text)):
        doc = {"author": quote_author[i], "quote": quote_text[i], "date": now}
        many_docs.append(doc)
    try:
        quotes_collection.insert_many(many_docs)
        print(f">>>> {len(many_docs) + last_posted_index} sended to db \n")
        return len(many_docs)
    except Exception as e:
        print(e)
        return 0

quote_list = []
author_list = []
last_posted_index = -1  # initialize with -1 since no quotes have been posted yet
for i in range(100):
    r = get_quote()
    print(f"{r} \n ")
    q_a = r.split("-")
    quote_list.append(q_a[0])
    author_list.append(q_a[1])
    ## API Usage Limit Tu connais xd
    if len(quote_list) % 5 == 0:  
        num_sent = post_quote(quote_text=quote_list, quote_author=author_list, last_posted_index=last_posted_index)
        last_posted_index += num_sent
        time.sleep(31)
