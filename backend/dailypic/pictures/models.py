from django.db import models
from django.contrib.auth import get_user_model
import environ
from dailypic.settings import STATIC_ROOT
import os

User = get_user_model()

env = environ.Env()
environ.Env.read_env()

IMAGES_URL = env('IMAGES_URL')

class Picture(models.Model):
    hashvalue = models.CharField(max_length=50, unique=True)
    path = models.FilePathField(unique=True)
    format = models.CharField(max_length=4)
    url = models.URLField(unique=True)
    thumbnail = models.URLField(unique=True)
    reported = models.BooleanField(default=False)
    query = models.CharField(max_length=50)
    download_url = models.URLField(unique=True)
    download_time = models.DateTimeField()

    # define values based on other values on save
    def save(self, *args, **kwargs):
        self.path = STATIC_ROOT + self.hashvalue + '.' + self.format
        self.url = IMAGES_URL + self.hashvalue + '.' + self.format
        self.thumbnail = IMAGES_URL + self.hashvalue + '.thumbnail.png'
        super().save(*args, **kwargs)

    # delete images from system filesystem on delete
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        if os.path.isfile(self.path):
            os.remove(self.path)
        if os.path.isfile(self.thumbnail):
            os.remove(self.thumbanil)
    
class Gallery(models.Model):
    title = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture, through='PictureOrder')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
class PictureOrder(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    date = models.DateField(null=True)
