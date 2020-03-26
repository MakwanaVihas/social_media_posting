from celery import shared_task
from time import sleep
from django.conf import settings
import requests
import twitter
import os

@shared_task
def upload_media_to_twitter(consumer_key, consumer_secret,real_oauth_token,real_oauth_token_secret,file_name=None,attachment_url=None,status=None):
    if file_name:
        api = twitter.Api(consumer_key, consumer_secret,real_oauth_token, real_oauth_token_secret)
        status = status if status else " "
        print(status)
        api.PostUpdate(status,media=open(settings.MEDIA_URL+"documents/"+file_name,"rb"),attachment_url=attachment_url)
        if os.path.exists(settings.MEDIA_ROOT+"/documents/"+file_name):
            os.remove(settings.MEDIA_ROOT+"/documents/"+file_name)
    else:
        api = twitter.Api(consumer_key, consumer_secret,real_oauth_token, real_oauth_token_secret)
        api.PostUpdate(status,attachment_url=attachment_url)

    return api
