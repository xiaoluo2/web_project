import requests
import random
import string

from PIL import Image
from imagehash import phash

import shutil
import os

api_url = 'https://www.googleapis.com/customsearch/v1'
api_key = 'AIzaSyAes6F5vryiG9LQoHDv6VGQScNoSb37Lto'
cx = '82405758baea9c02b'

# tempory download location
tmp_root = '/var/www/data/tmp/'
# image storage location
img_root = '/var/www/data/images/'

# obtains image url from Google Custom Search API
def get_img_url(query):
    start = random.randint(0,99)
    payload = {'key': api_key, 'cx': cx, 'q': query, 'searchType': 'image', 'start': start, 'num':'1'}

    res = requests.get(api_url, params = payload)
    js = res.json()
    img_url = js['items'][0]['link']
    del res

    return img_url

# Downloads image to temporary folder
def download_img(url):
    # changed to random file name to make race conditions less likely
    filename = random.choices(string.ascii_letters + string.digits, k=3)
    img_path = tmp_root + filename

    res = requests.get(url, stream=True)
    f = open(img_path, 'wb')

    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, f)
    del res

    return img_path

# return pillow image
def open_image(img_path):
    return Image.open(img_path)

# return perceptual hash string
def hash_image(img):
    return str(imagehash.phash(img))

# saves image in appropriate format and location
def save_image(img, max_size, filename, format):
    # resize image, note: thumbnail just downsizes keeping aspect ratio
    img.thumbnail(max_size)
    img.save(img_root + filename, format=format)
