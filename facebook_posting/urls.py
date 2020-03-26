from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


fb_list = views.FBModelViewSet.as_view({
    "get":"list","post":"create"
})

fb_detail = views.FBModelViewSet.as_view({'get': 'retrieve',
                                          'put': 'update',
                                          'patch': 'partial_update',
                                          'delete': 'destroy'})

urlpatterns = [
    path("facebook/login/",views.login,name="facebook"),
    path("facebook/logged_in/",views.logged_in),
    path("facebook/upload_facebook/",views.upload,name="upload_facebook"),

    # path("rest/facebook/",fb_list),
    # path("rest/facebook/<int:id>",fb_detail),

]
