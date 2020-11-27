import requests
import random
import string
import shutil
import os
import logging
from datetime import datetime
import environ
from celery import shared_task, chain, group
from dailypic.settings import STATIC_ROOT
from PIL import Image
from imagehash import phash
from django.core import serializers
from pictures.models import Picture

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)

# Google Custom Search API
API_URL = 'https://www.googleapis.com/customsearch/v1'
API_KEY = env('GOOGLE_API_KEY')
CX = env('GOOGLE_CX')
IMAGE_URL = 'images.dailypicture.xyz/images/' 

# max image size
MAX_SIZE = 1920, 1080
# max thumbnail size
THB_SIZE = 250, 250

# pull N images
@shared_task
def pull_images(query, N):
    group(pull_image.s(query) for i in range(N))
    group()

# calls chain of tasks to pull image and returns Picture object
@shared_task
def pull_image(query):
    chain = get_img_url.s(query) | was_downloaded.s() | download_img.s() | compare_img.s() | save_img.s() | create_object.s()
    chain()

# deserialize picture data and create object
@shared_task
def create_object(picdata):
    pic = Picture(
            url = IMAGE_URL + picdata['hashvalue'] '.' + picdata['format'].lower(),
            query = picdata['query'],
            format = picdata['format'],
            path = picdata['path'],
            hashvalue = picdata['hashvalue'],
            download_url = picdata['download_url'],
            download_time = picdata['download_time'],
            )
    pic.save()
    return pic.pk

# obtains image url from Google Custom Search API
@shared_task
def get_img_url(query):
    start = random.randint(0,99)
    payload = {'key': API_KEY, 'cx': CX, 'q': query, 'searchType': 'image', 'start': start, 'num':'1'}

    res = requests.get(API_URL, params = payload)
    js = res.json()
    img_url = js['items'][0]['link']
    del res
    # json to pass through task chain
    picdata = {'download_url': img_url, 'query': query}
    return picdata

# check if image has been downloaded
@shared_task(bind=True)
def was_downloaded(self, picdata):
    try:
        pic = Picture.objects.get(url=picdata['download_url'])
    except Picture.DoesNotExist:
        pic = None
    if pic is not None and pic.exists():
        logger.info('Image previously downloaded.')
        # stop task chain
        self.request.callbacks = None
        return pic.id
    return picdata

# download image to temporary folder
@shared_task
def download_img(picdata):

    # get file extension
    url = picdata['download_url']
    filename = url.split('/')[-1]

    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    picdata['path'] = STATIC_ROOT + 'tmp/' + random_name 

    res = requests.get(url, stream=True)
    f = open(picdata['path'], 'wb')

    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, f)
    del res

    picdata['download_time'] = datetime.now()

    return picdata

# return perceptual hash string
# :img: PIL Image
@shared_task(bind=True)
def compare_img(self, picdata):
    img = Image.open(picdata['path'])
    picdata['hashvalue'] = str(phash(img))
    img.close()
    # check if similar image exists
    try:
        pic = Picture.objects.get(hashvalue=hash)
    except Picture.DoesNotExist:
        pic = None
    if pic is not None and pic.exists():
        logger.info('Similar image exists.')
        # stop task chain
        self.request.callbacks = None
        return pic.id
    
    # passing path location through the chain
    return picdata

# saves image and thumbnail in appropriate format and location
# :return:path of saved image if successful, None on fail
@shared_task
def save_img(picdata):
    img = Image.open(picdata['path'])
    picdata['format'] = img.format
    # save image
    img.thumbnail(MAX_SIZE)
    path = STATIC_ROOT + 'images/' + picdata['hashvalue'] + '.' + img.format.lower()
    img.save(path)
    picdata['path'] = path
    # save thumbnail
    img.thumbnail(THB_SIZE)
    path = STATIC_ROOT + 'images/' + picdata['hashvalue'] + '.thumbnail.png' 
    img.save(path, format='PNG')
    return picdata 
