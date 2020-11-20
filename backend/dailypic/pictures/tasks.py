from celery import shared_task 
from models import Picture
import image_utils
from datetime import datetime

@shared_task
def pull_image(query):
     img = download_img(get_img_url(query))
     hash_value = hash_img(img)
     loc = move_img(img, hash_value)

     Picture.objects.create(
             hashvalue = hash_value,
             file_path = loc,
             download_date = datetime.utcnow()
             )
