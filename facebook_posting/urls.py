from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("facebook/login",views.login,name="facebook"),
    path("facebook/logged_in",views.logged_in),
    path("facebook/upload_facebook",views.upload,name="upload_facebook")
]
