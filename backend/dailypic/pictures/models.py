from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Picture(models.Model):
    hashvalue = models.CharField(max_length=16, unique=True)
    path = models.FilePathField(unique=True)
    format = models.CharField(max_length=4)
    url = models.URLField(unique=True)
    reported = models.BooleanField(default=False)
    query = models.CharField(max_length=50)
    download_url = models.URLField(unique=True)
    download_time = models.DateTimeField()
    
class Gallery(models.Model):
    title = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture, through='PictureOrder')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
class PictureOrder(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    date = models.DateField(null=True)
