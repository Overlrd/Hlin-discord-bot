import random

from googleapiclient import discovery

from settings import CUSTOM_SEARCH_WONDERMIND_URL

def search_feeling(q, cx, key, num=10, start=1, linksite= CUSTOM_SEARCH_WONDERMIND_URL , alt='json'):
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

