from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import facebook
import requests
from django.conf import settings
import datetime
from .tasks import upload_media_to_facebook
from .forms import FBFileSchedularForm
from rest_framework import status, renderers
from rest_framework.viewsets import ModelViewSet
from .serializers import FBFileSchedularModelSerializer
from .models import FBFileSchedularModel
from rest_framework.decorators import action


perms = ["manage_pages","publish_pages"]
app_id = "YOUR_APP_ID"
canvas_url = "https://127.0.0.1:8000/facebook/logged_in"

def login(request):
    graph = facebook.GraphAPI(access_token="YOUR_ACCESS_TOKEN")
    fb_login_url = graph.get_auth_url(app_id,canvas_url,perms)
    return HttpResponseRedirect(fb_login_url)

def logged_in(request):
    request.session["code"] = request.GET["code"]
    # return HttpResponse(request.session["code"])
    return HttpResponseRedirect(reverse("upload_facebook"))

def upload(request):
    id_names={}
    id_tokens={}

    if request.method == "POST":
        form = FBFileSchedularForm(request.POST,request.FILES)
        if form.is_valid():
            time = request.POST["form-control"]
            time = time.split(" ")
            scheduled_date = time[0].split("/")
            scheduled_time = time[1].split(":")

            current_ = datetime.datetime(year = int(scheduled_date[-1]),month=int(scheduled_date[1]),day = int(scheduled_date[0]),hour=int(scheduled_time[0]),minute=int(scheduled_time[1]),second=59)
            delta = current_ - datetime.datetime.now()
            delta = datetime.datetime.utcnow()+delta

            fs = form.cleaned_data['file_field']
            url_ = None if form.cleaned_data['url_field']=="" else form.cleaned_data['url_field']
            post_ = None if form.cleaned_data['text_field']=="" else form.cleaned_data['text_field']
            page = request.session["id_dict"][request.POST["page_id"]]
            page_token = request.session["token_dict"][str(page)]
            form.save()

            if not fs:
                upload_media_to_facebook.apply_async(args=(page_token,page,post_,url_,None),eta=delta)
            else:
                fs.name = fs.name.replace(" ","_")
                upload_media_to_facebook.apply_async(args=(page_token,page,post_,url_,settings.MEDIA_URL+"facebook/"+fs.name),eta=delta)

        else:
            return render(request,"form_fb.html",{"form":form,"id_names":list(request.session["id_dict"].keys())})

    else:
        code = request.session["code"]
        req = requests.post("https://graph.facebook.com/v6.0/oauth/access_token",params={
                "client_id":"2545738395649512",
                "redirect_uri":canvas_url,
                "client_secret":"c437d9f712c0f3c39e718c85bee11778",
                "code":code,
        })

        access_token = req.json()["access_token"]


        req = requests.get("https://graph.facebook.com/v6.0/me/accounts",params={"access_token":access_token})
        for i in req.json()["data"]:
            id_names[str(i["name"])] = int(i["id"])
            id_tokens[int(i["id"])] = str(i["access_token"])

        request.session["token_dict"] = id_tokens
        request.session["id_dict"] = id_names

        form = FBFileSchedularForm()
        return render(request,"form_fb.html",{"form":form,"id_names":list(id_names.keys())})

    return render(request,"form_fb.html",{"form":form,"id_names":list(request.session["id_dict"].keys())})


class FBModelViewSet(ModelViewSet):
    serializer_class = FBFileSchedularModelSerializer
    queryset = FBFileSchedularModel.objects.all()

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def create(self,request):
        serializer = FBFileSchedularModelSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.data['schedule_time'])
            time_ = serializer.data['schedule_time'].split("+")[0].replace("T"," ")
            time_ = datetime.datetime.strptime(time_, "%Y-%m-%d %H:%M:%S")
            delta = time_ - datetime.datetime.now()
            delta = datetime.datetime.utcnow()+delta

            fs = serializer.data['file_field']
            url_ = None if serializer.data['url_field']=="" else serializer.data['url_field']
            post_ = None if serializer.data['text_field']=="" else serializer.data['text_field']

            page = request.session["id_dict"][request.POST["page_id"]]
            page_token = request.session["token_dict"][str(page)]

            if not fs:
                upload_media_to_facebook.apply_async(args=(page_token,page,post_,url_,None),eta=delta)
            else:
                upload_media_to_facebook.apply_async(args=(page_token,page,post_,url_,settings.MEDIA_URL+"facebook/"+fs.name),eta=delta)
        return super().create(request)
