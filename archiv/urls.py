from django.conf.urls import url
from . import views

app_name = 'archiv'

urlpatterns = [
    url(
        r'^archresource/$',
        views.ArchResourceListView.as_view(),
        name='archresource_browse'
    ),
    url(
        r'^subject-cloud/$',
        views.subject_cloud,
        name='subject-cloud'
    ),
    url(
        r'^schlagworte/$',
        views.SchlagwortList.as_view(),
        name='schlagworte'
    ),
    url(
        r'^archresource/detail/(?P<pk>[0-9]+)$',
        views.ArchResourceDetailView.as_view(),
        name='archresource_detail'
    ),
    url(
        r'^archresource/create/$',
        views.ArchResourceCreate.as_view(),
        name='archresource_create'
    ),
    url(
        r'^archresource/edit/(?P<pk>[0-9]+)$',
        views.ArchResourceUpdate.as_view(),
        name='archresource_edit'
    ),
    url(
        r'^archresource/delete/(?P<pk>[0-9]+)$',
        views.ArchResourceDelete.as_view(),
        name='archresource_delete'),
]
