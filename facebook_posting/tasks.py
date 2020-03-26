from celery import shared_task
from time import sleep
from django.conf import settings
import requests
import os

@shared_task
def upload_media_to_facebook(page_access_token,id,message=None,link=None,url=None):

    print(page_access_token,id,message,link,url)
    if url:
        if url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".JPG") or url.endswith(".JPEG") or url.endswith(".PNG"):
            req = requests.post("https://graph.facebook.com/{}/photos".format(str(id)),params = {"access_token":page_access_token,"caption":message},files={"file":open(url,"rb")})
            print(req.text)
            return req.json()
        elif url.endswith(".mp4") or url.endswith(".mov") or url.endswith(".MP4") or url.endswith(".MOV"):
            req = requests.post("https://graph-video.facebook.com/{}/videos".format(str(id)),params={"access_token":page_access_token,"description":message},file={"file":open(url,"rb")})
            return req.json()

    elif link:
        req = requests.post("https://graph.facebook.com/{}/feed".format(str(id)),params = {"message":message,"access_token":page_access_token,"link":link})
        return req.json()
    else:
        req = requests.post("https://graph.facebook.com/{}/feed".format(str(id)),params = {"access_token":page_access_token,"message":message})
        return req.json()
