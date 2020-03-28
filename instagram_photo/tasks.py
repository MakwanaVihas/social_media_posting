from celery import shared_task
from time import sleep
from django.conf import settings
from django.shortcuts import reverse
import requests

import twitter
import os
from instabot import Bot
from django.http import HttpResponse,HttpResponseRedirect

from PIL import Image

@shared_task
def upload_media_to_insta(username,password,file_name,caption=None):
    bot = Bot()
    bot.login(username = username,password = password)

    image = Image.open(settings.MEDIA_ROOT+"/instagram/"+file_name)
    image = image.resize((600,600))
    image = image.convert('RGB')
    image.save(settings.MEDIA_ROOT+"/instagram/"+file_name)
    print(settings.MEDIA_ROOT+"/instagram/"+file_name)


    bot.upload_photo(settings.MEDIA_URL+"instagram/"+file_name,caption=caption)
    return "ok"
