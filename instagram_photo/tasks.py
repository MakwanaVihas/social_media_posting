from celery import shared_task
from time import sleep
from django.conf import settings
import requests
import twitter
import os
from PIL import Image

@shared_task
def upload_media_to_insta(bot,file_name,caption=None):

    image = Image.open(settings.MEDIA_ROOT+"/instagram/"+file_name)
    image = image.resize((600,600))
    image = image.convert('RGB')
    image.save(settings.MEDIA_ROOT+"/instagram/"+file_name)
    print(settings.MEDIA_ROOT+"/instagram/"+file_name)


    bot.upload_photo(settings.MEDIA_URL+"instagram/"+file_name,caption=caption)
    return "ok"
