from django.urls import path
from . import views

urlpatterns = [
    path("insta/login/",views.login_view,name="login_insta"),
    path("insta/check/",views.logged_in,name="insta_logged_in"),
    path("insta/upload/",views.upload_insta,name="upload_insta"),
    path("insta/log_out_insta/",views.log_out_insta,name="log_out_insta")


]
