import requests
import random

from PIL import Image
from imagehash import phash

import shutil
import os

api_url = 'https://www.googleapis.com/customsearch/v1'
api_key = 'AIzaSyAes6F5vryiG9LQoHDv6VGQScNoSb37Lto'
cx = '82405758baea9c02b'

tmp_root = '/data/tmp/'
img_root = '/data/images/'

def get_img_url(query):
    start = random.randint(0,99)
    payload = {'key': api_key, 'cx': cx, 'q': query, 'searchType': 'image', 'start': start, 'num':'1'}

    res = requests.get(api_url, params = payload)
    js = res.json()
    img_url = js['items'][0]['link']
    del res

    return img_url

def download_img(url):
    filename = url.split('/')[-1]
    img_path = tmp_root + filename

    res = requests.get(url, stream=True)
    f = open(img_path, 'wb')
    
    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, f)
    del res

    return img_path

def hash_img(img_path):
    img = Image.open(img_path)
    img.show()
    hash_value = phash(img)
    return str(hash_value)

def move_img(img_path, filename):
    target = img_root + filename
    if not os.path.exists(target):
        os.rename(img_path, target)
        return target
    else:
        return None
