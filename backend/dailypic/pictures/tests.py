from django.test import TestCase
from .tasks import pull_image, get_img_url, download_img, compare_img, save_img, was_downloaded
from celery import chain

from PIL import Image
import os

max_width, max_height = 1920, 1080

class PictureTestCase(TestCase):

    def test_pull_image(self):
        r = pull_image('cat')
        id = r.get()
        self.assertIsNotNone(id)

#    def test_url_exists(self):
#        task = was_downloaded.delay({'download_url': 'https://cdn.cnn.com/cnnnext/dam/assets/190718181632-cats-movie-trailer-exlarge-169.jpg'})
#        result = task.get()
#        self.assertEqual(result,  5)
