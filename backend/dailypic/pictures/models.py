from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
    hashvalue = models.CharField(max_length=16, unique=True)
    path = models.FilePathField(unique=True)
    url = models.URLField(unique=True)
    reported = models.BooleanField(default=False)
    download_url = models.URLField(unique=True)
    download_date = models.DateField()
    
class Gallery(models.Model):
    title = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture, through='GalleryOrder')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class GalleryOrder(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    order = models.IntegerField()
