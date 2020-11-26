from celery import shared_task
import requests
import random
import string
from PIL import Image
from imagehash import phash
import shutil
import os
import logging
import datetime
import environ
from dailypic.settings import STATIC_ROOT

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)


# Google Custom Search API
api_url = 'https://www.googleapis.com/customsearch/v1'
api_key = env('GOOGLE_API_KEY')
cx = env('GOOGLE_CX')

# max image size
max_size = 1920, 1080
# max thumbnail size
thumb_size = 250, 250

@shared_task
def sample_task():
    print('sample task was run')

# calls chain of tasks to pull image and returns Picture object
@shared_task
def pull_image(query):
    # get url from google api
    r= get_img_url.delay(query)
    d_url= r.get()

    # check if picture was previously downloaded
    try:
        pic = Picture.objects.get(url=d_url)
    except Picture.DoesNotExist:
        logger.error('Class Picture does not exist.')
    if pic.exists():
        logger.info('Image previously downloaded.')
        return pic

    r = download_img.delay(d_url)
    tmp_path = r.get()

    # create perceptual hash
    r= hash_img.delay(tmp_path)
    hvalue = r.get()

    # check if similar image exists
    try:
        pic = Picture.objects.get(hashvalue=hvalue)
    except Picture.DoesNotExist:
        logger.error('Class Picture does not exist.')
    if pic.exists():
        logger.info('Similar image exists in database')
        return pic

    save_image.delay(tmp_path, hvalue + '.thumbnail', thumb_size, 'png')
    r = save_image.delay(tmp_path, hvalue, max_size, format=None)
    new_path = r.get()

    # create and return Picture object
    Picture.objects.create(
            hashvalue=hvalue,
            path = new_path,
            url = STATIC_ROOT + 'images/' + hvalue,
            query = query,
            download_url = d_url,
            download_time = datetime.now()
            )

    return pic

# obtains image url from Google Custom Search API
@shared_task
def get_img_url(query):
    start = random.randint(0,99)
    payload = {'key': api_key, 'cx': cx, 'q': query, 'searchType': 'image', 'start': start, 'num':'1'}

    res = requests.get(api_url, params = payload)
    js = res.json()
    img_url = js['items'][0]['link']
    del res

    return img_url

# download image to temporary folder
@shared_task
def download_img(url):

    # get file extension
    filename = url.split('/')[-1]
    format = filename.split('.')[-1]

    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    tmp_path = STATIC_ROOT + 'tmp/' + random_name + '.' + format

    res = requests.get(url, stream=True)
    f = open(tmp_path, 'wb')

    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, f)
    del res

    return tmp_path

# return perceptual hash string
# :img: PIL Image
@shared_task
def hash_image(path):
    img = Image.open(path)
    return str(phash(img))

# resizes and saves image in appropriate format and location
# :return:path of saved image if successful, None on fail
@shared_task
def save_image(src, filename, size, format=None):
    img = Image.open(src)
    img = img.thumbnail(size)
    if format is None:
        format = img.format.lower()
    path = STATIC_ROOT + 'images/' + filename + '.' + format
    img.save(path, format=format)
    if not os.path.exists(path):
        return None
    return path
