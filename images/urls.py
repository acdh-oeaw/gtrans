from django.conf.urls import url
from . import views

app_name = 'images'

urlpatterns = [
    url(r'^$', views.ImageListView.as_view(), name='image_list'),
    url(r'^(?P<pk>[0-9]+)$', views.ImageDetailView.as_view(), name='image_detail'),
    url(r'^create/$', views.ImageCreate.as_view(), name='image_create'),
    url(r'^zipupload/$', views.UploadZip.as_view(), name='image_zipupload'),
    # url(r'^create/$', views.ImageCreate.as_view(), name='image_create'),
    # url(r'^update/(?P<pk>[0-9]+)$', views.ImageUpdate.as_view(), name='image_update'),
]
