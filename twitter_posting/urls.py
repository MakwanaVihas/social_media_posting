from . import views
from facebook_posting.views import FBModelViewSet
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'twitter', views.FileSchedularViewSet)
router.register(r'facebook', FBModelViewSet)


tw_detail = views.FileSchedularViewSet.as_view({'get': 'retrieve',
                                                 'put': 'update',
                                                 'patch': 'partial_update',
                                                 'delete': 'destroy'})
tw_list = views.FileSchedularViewSet.as_view({'get': 'list',
                                                 'post': 'create',
                                                 })


urlpatterns = [
    path('twitter/login/',views.login,name="twitter"),
    path('twitter/logged_in/',views.logged_in,name="logged_in"),
    path('twitter/upload/',views.upload_media,name = "upload"),
    path('twitter/logout/',views.deactivate,name = "logout"),

    # path("rest/twitter/",tw_list),
    # path("rest/twitter/<int:id>",tw_detail)
    path('rest/',include(router.urls))

    # path('rest/twitter/',views.FileSchedularSerializerView.as_view()),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
