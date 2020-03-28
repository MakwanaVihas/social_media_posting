from django.shortcuts import render,reverse
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from instabot import Bot
import urllib
from .forms import InstaFileSchedularForm,InstaFileSchedular
from .tasks import upload_media_to_insta
import datetime
# Create your views here.

bot = Bot()

@csrf_exempt
def login_view(request):
    if "my_context" in request.GET:
        print(request.GET["my_context"])
        return render(request,"login_insta.html",context={"context":request.GET["my_context"]})

    return render(request,"login_insta.html")


def logged_in(request):
    if request.method == "POST":
        try:
            print(request.POST["username"],request.POST["password"])
            bot.login(username = request.POST["username"],password = request.POST["password"])
            request.session["username"] = request.POST["username"]
            request.session["password"] = request.POST["password"]

            return HttpResponseRedirect(reverse("upload_insta"))

        except SystemExit:
            return redirect('/insta/login?' + urllib.parse.urlencode({"my_context":"Invalid Context"}))
    else:
        return redirect('/insta/login')

def log_out_insta(request):
    try:
        bot.logout()
        if "username" in request.session.keys(): del request.session["username"]
        if "password" in request.session.keys(): del request.session["password"]
    except AttributeError:
        pass

    return redirect('/insta/login')

def upload_insta(request):

    try:
        bot.get_your_medias()
    except AttributeError:
        return HttpResponseRedirect(reverse("login_insta"))
    if request.method == "POST":
        form = InstaFileSchedularForm(request.POST,request.FILES)
        if form.is_valid():
            time = request.POST["form-control"]
            time = time.split(" ")
            scheduled_date = time[0].split("/")
            scheduled_time = time[1].split(":")

            current_ = datetime.datetime(year = int(scheduled_date[-1]),month=int(scheduled_date[1]),day = int(scheduled_date[0]),hour=int(scheduled_time[0]),minute=int(scheduled_time[1])+1,second=59)
            delta = current_ - datetime.datetime.now()
            delta = datetime.datetime.utcnow()+delta

            file_ = form.cleaned_data["file_field"]
            caption = None if form.cleaned_data['text_field']=="" else form.cleaned_data['text_field']
            form.save()

            upload_media_to_insta.apply_async(args=(request.session["username"],request.session["password"],file_.name.replace(" ","_"),caption),eta=delta)
        else:
            return render(request,"form.html",context={"form":form})

    else:
        form = InstaFileSchedularForm()

    return render(request,"form_insta.html",context={"form":form})
