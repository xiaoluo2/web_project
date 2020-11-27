from django.test import TestCase
from dailypic.celery import app
from .tasks import pull_image, get_img_url, download_img, compare_img, save_img

from PIL import Image
import os

max_width, max_height = 1920, 1080

class PullTestCase(TestCase):
    def test_pull_image(self):
        task = pull_image.s().apply(args=['cat'])
        self.assertEqual(task.result, 'SUCESS')

