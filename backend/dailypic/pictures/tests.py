from django.test import TestCase
from .tasks import pull_image, get_img_url, download_img, compare_img, save_img, was_downloaded, break_chain, test_task, last_task
from celery.result import AsyncResult
from celery import chain

from PIL import Image
import os

max_width, max_height = 1920, 1080

class CeleryTestCase(TestCase):
    def test_pull_image(self):
        task = pull_image.delay('cat')
        id = task.get()
        res = AsyncResult(id).get()
        self.assertIsNotNone(res)

    def test_url_exists(self):
        task = was_downloaded.delay({'download_url': 'https://cdn.cnn.com/cnnnext/dam/assets/190718181632-cats-movie-trailer-exlarge-169.jpg'})
        result = task.get()
        self.assertEqual(result,  5)

    def test_chain_break(self):
        chain = (break_chain.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|last_task.si())
        chain()
