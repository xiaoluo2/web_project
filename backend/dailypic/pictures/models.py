from django.db import models
from django_celery_beat.models import PeriodicTask
from django.contrib.auth.models import User

class Picture(models.Model):
    hashvalue = models.CharField(max_length=16, unique=True)
    file_path = models.FilePathField(max_length=50, unique=True)
    reported = models.BooleanField(default=False)
    download_date = models.DateField()

class Gallery(models.Model):
    title = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
