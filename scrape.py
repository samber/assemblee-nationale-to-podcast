
import os
import time
from dateutil.parser import parse

import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

SCRAPING_DELAY = int(os.environ['SCRAPING_DELAY']) if 'SCRAPING_DELAY' in os.environ else 2

def do_req(url):
    time.sleep(SCRAPING_DELAY)
    r = requests.get(url, allow_redirects=True)
    return BeautifulSoup(r.text, 'html.parser')

def list_last_commissions():
    html = do_req('http://videos.assemblee-nationale.fr/commissions')
    items = html.select('#myCarousel-contenu .span4')
    return map(lambda item: item.select('.vl')[0].attrs['href'], items)

def get_commission_details(path):
    html = do_req('http://videos.assemblee-nationale.fr/' + path)

    # stop scraping if it's a live video
    if len(html.select('meta[itemprop=contentURL]')) == 0:
        print('Waiting live video:', html.select('meta[itemprop=name]')[0].attrs['content'])
        return None

    name = html.select('meta[itemprop=name]')[0].attrs['content']
    thumbnailUrl = html.select('meta[itemprop=thumbnailUrl]')[0].attrs['content']
    contentURL = html.select('meta[itemprop=contentURL]')[0].attrs['content']
    uploadDate = html.select('meta[itemprop=uploadDate]')[0].attrs['content']

    return {
        "name": name,
        "image": thumbnailUrl,
        "url": contentURL.replace('_1.mp4', '.mp3'),
        "date": parse(uploadDate.replace('CET', ' ')),
    }

def list_all_commissions_with_details(since=None):
    paths = list(list_last_commissions())
    paths.reverse() # reverse order: oldest to newest

    # get full details for each commission
    details = []
    for path in paths:
        detail = get_commission_details(path)
        # if it is a live commission, then stop scraping
        if detail is None:
            break
        details.append(detail)

    if since is None:
        return details

    return filter(lambda detail: detail['date']>since, details)
