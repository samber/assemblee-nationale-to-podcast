
from datetime import datetime, timedelta
import os
import tempfile
import traceback
import asyncio
import time

import requests

from scrape import list_all_commissions_with_details
from audio import trim_silence
from anchorfm import upload_podcast_to_anchor

ENV = os.environ['ENV']

def download_audio(url):
    r = requests.get(url, allow_redirects=True)
    new_file, filename = tempfile.mkstemp()
    os.write(new_file, r.content)

    os.close(new_file)
    return filename

async def run_job():
    SCRAPE_SINCE = datetime.now()
    if ENV == 'dev':
        SCRAPE_SINCE = SCRAPE_SINCE - timedelta(10) # past 10 days

    while True:
        videos = list_all_commissions_with_details(SCRAPE_SINCE)
        for video in videos:
            try:
                print("**** NEW VIDEO ****")
                print(video['date'], video['name'])

                print("**** DOWNLOADING ****")
                audio_file = download_audio(video['url'])
                video['local_file'] = audio_file
                print('tmp file:', video['local_file'])

                print("**** REMOVE SILENCES ****")
                video['timmmed_local_file'] = trim_silence(audio_file)

                print("**** UPLOADING ****")
                await upload_podcast_to_anchor(video)
                print("**** VIDEO END ****")

                SCRAPE_SINCE = video['date']
            except Exception as err:
                print(err)
                traceback.print_exc()

            try:
                if 'local_file' in video:
                    os.remove(video['local_file'])
                if 'timmmed_local_file' in video:
                    os.remove(video['timmmed_local_file'])
            except Exception as err:
                print(err)
                traceback.print_exc()


        time.sleep(10*60)   # 10 minutes


def start_worker():
    asyncio.run(run_job())
