from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status,renderers
from .serializers import FileSchedularModelSerializer
from . models import FileSchedularModel

import os
import urllib
import twitter
from .forms import FileSchedularForm
from .tasks import upload_media_to_twitter
import requests
import oauth2 as oauth
import datetime
import pytz
from requests_oauthlib import OAuth1
from rest_framework.decorators import action


request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

consumer_key = "YOUR_KEY"
consumer_secret = "YOUR_SECRET"


def login(request):

    consumer = oauth.Consumer(consumer_key,consumer_secret)
    client = oauth.Client(consumer)
    esp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({
                                   "oauth_callback": request.build_absolute_uri(reverse("logged_in"))}))
    # print(request.build_absolute_uri(reverse("logged_in")))
    # return HttpResponse(content)
    request_token = dict(urllib.parse.parse_qsl(content))
    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')
    request.session['oauth_token_secret'] = oauth_token_secret

    return HttpResponseRedirect(authorize_url+"?oauth_token="+oauth_token)

def logged_in(request):


    oauth_token = request.GET["oauth_token"]
    oauth_verifier = request.GET["oauth_verifier"]
    oauth_token_secret = request.session['oauth_token_secret']
    consumer = oauth.Consumer(consumer_key, consumer_secret)

    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST")

    access_token = dict(urllib.parse.parse_qsl(content))
    screen_name = access_token[b'screen_name'].decode('utf-8')
    user_id = access_token[b'user_id'].decode('utf-8')

    real_oauth_token = access_token[b'oauth_token'].decode('utf-8')
    real_oauth_token_secret = access_token[b'oauth_token_secret'].decode(
        'utf-8')


    request.session["real_oauth_token"] = real_oauth_token
    request.session["real_oauth_token_secret"] = real_oauth_token_secret
    request.session["oauth_token"] = oauth_token
    request.session["oauth_verifier"] = oauth_verifier

    return HttpResponseRedirect(reverse("upload"))


def deactivate(request):
    url = "https://api.twitter.com/1.1/oauth/invalidate_token"
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    auth = oauth.Token(request.session["real_oauth_token"],request.session["real_oauth_token_secret"])
    client = oauth.Client(consumer, auth)
    resp, con = client.request(url,"POST")

    if "real_oauth_token" in request.session:
        del request.session["real_oauth_token"]
        del request.session["real_oauth_token_secret"]
        del request.session["oauth_verifier"]


    return HttpResponseRedirect(reverse("starting_page"))

@csrf_exempt
def upload_media(request):
    if request.session["real_oauth_token_secret"]==None or request.session["real_oauth_token"] == None:
        return HttpResponse("PLEASE AUTHORIZE")
    if request.method == "POST":
        form = FileSchedularForm(request.POST,request.FILES)


        if form.is_valid():
            time = request.POST["form-control"]
            time = time.split(" ")
            scheduled_date = time[0].split("/")
            scheduled_time = time[1].split(":")

            current_ = datetime.datetime(year = int(scheduled_date[-1]),month=int(scheduled_date[1]),day = int(scheduled_date[0]),hour=int(scheduled_time[0]),minute=int(scheduled_time[1])+1,second=59)
            delta = current_ - datetime.datetime.now()
            delta = datetime.datetime.utcnow()+delta

            fs = form.cleaned_data['file_field']
            url_ = None if form.cleaned_data['url_field']=="" else form.cleaned_data['url_field']
            tweet_ = None if form.cleaned_data['text_field']=="" else form.cleaned_data['text_field']
            form.save()
            if fs:
                fs.name = fs.name.replace(" ","_")
                upload_media_to_twitter.apply_async(args=(consumer_key,consumer_secret,request.session["real_oauth_token"],request.session["real_oauth_token_secret"],fs.name,url_,tweet_),eta=delta)
            else:
                upload_media_to_twitter.apply_async(args=(consumer_key,consumer_secret,request.session["real_oauth_token"],request.session["real_oauth_token_secret"],None,url_,tweet_),eta=delta)
        else:
            return render(request,"form.html",context={"form":form})

    else:
        form = FileSchedularForm()

    return render(request,"form.html",context={"form":form})



class FileSchedularSerializerView(APIView):
    def get(self, request, format=None):
        snippets = FileSchedularModel.objects.all()
        serializer = FileSchedularModelSerializer(snippets, many=True)
        return Response(serializer.data)
    def post(self,requests,format=None):
        serializer = FileSchedularSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileSchedularViewSet(ModelViewSet):
    serializer_class = FileSchedularModelSerializer
    queryset = FileSchedularModel.objects.all()


    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


    def create(self, request):

        serializer = FileSchedularModelSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.data['schedule_time'])
            time_ = serializer.data['schedule_time'].split("+")[0].replace("T"," ")
            time_ = datetime.datetime.strptime(time_, "%Y-%m-%d %H:%M:%S")
            delta = time_ - datetime.datetime.now()
            delta = datetime.datetime.utcnow()+delta

            fs = serializer.data['file_field']
            url_ = None if serializer.data['url_field']=="" else serializer.data['url_field']
            tweet_ = None if serializer.data['text_field']=="" else serializer.data['text_field']

            if fs:
                fs.name = fs.name.replace(" ","_")
                upload_media_to_twitter.apply_async(args=(consumer_key,consumer_secret,request.session["real_oauth_token"],request.session["real_oauth_token_secret"],fs.name,url_,tweet_),eta=delta)
            else:
                upload_media_to_twitter.apply_async(args=(consumer_key,consumer_secret,request.session["real_oauth_token"],request.session["real_oauth_token_secret"],None,url_,tweet_),eta=delta)

        return super().create(request)
