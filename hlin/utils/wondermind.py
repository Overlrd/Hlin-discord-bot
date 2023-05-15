import random

from googleapiclient import discovery

from config import WONDERMIND_ENDPOINT  #  ss

def search_by_feelings(q, cx, key, num=10, start=1, linksite= WONDERMIND_ENDPOINT , alt='json'):
    search_params = {
        'q': q,
        'cx': cx,
        'key': key,
        'num': num,
        'start': start,
        'alt': alt,
        'linkSite': linksite
    }
    service = discovery.build("customsearch", "v1", developerKey=search_params['key'])

    res = service.cse().list(q=search_params['q'], cx=search_params['cx'],
                             num=search_params['num'], start=search_params['start'],
                             alt=search_params['alt']).execute()

    item = random.choice(res['items'])
    return item

