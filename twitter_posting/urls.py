from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('twitter/login',views.login,name="twitter"),
    path('twitter/logged_in',views.logged_in,name="logged_in"),
    path('twitter/upload/',views.upload_media,name = "upload"),
    path("rest/twitter/",views.FileSchedularViewSet.as_view({'get': 'list', 'post':'create'}))
    # path('rest/twitter/',views.FileSchedularSerializerView.as_view()),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
