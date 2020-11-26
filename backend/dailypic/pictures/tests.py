from django.test import TestCase
from dailypic.celery import app
from tasks import pull_image
from tasks import get_img_url
from tasks import download_img
from tasks import hash_image
from tasks import resize
from tasks import save_image

from PIL import Image
import os

max_width = 100
max_height = 100

class TasksTestCase(TestCase):
        
    def test_get_img_url(self):
        task = get_img_url.s().apply(args=['cat'])
        self.assertEqual(task.result, 'SUCESS')

    def test_download_img(self):
        task = download_img.s()
        res = task.apply(args=['https://static.toiimg.com/photo/msid-67586673/67586673.jpg?3918697'])
        tmp_path = res.get()
        self.assertTrue(os.path.exists(tmp_path))
        self.assertEqual(task.result, 'SUCESS')

    def test_hash_image(self):
        task = hash_image.s()
        img = Image.open()
        res = task.apply(args=['/home/xiao/cat.jpeg'])
        hash = res.get()
        self.assertEqual(hash, 'e598d99c9b318696')
        self.assertEqual(task.result, 'SUCESS')

    def test_save_image(self):
        task = save_image.s()
        res = task.apply(args=['/home/xiao/cat.jpeg', '/home/xiao/cat-copy.png', (max_width, max_length)], kwargs={'format': 'PNG'})
        self.assertEqual(task.result, 'SUCESS')
        
        img = Image.open(res.get())
        # check size requirements
        width, height = img.size()
        self.assertTrue(width < max_width)
        self.assertTrue(height < max_height)
        # file exists
        self.assertTrue(os.path.exists('/home/xiao/cat-copy.png'))

class PullImageTestCase(TestCase):
    def test_pull_image(self):
        task = pull_image.s().apply(args=['cat'])
        self.assertEqual(task.result, 'SUCESS')

