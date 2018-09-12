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
    url(
        r'^repolocation/$',
        views.RepoLocationListView.as_view(),
        name='repolocation_browse'
    ),
    url(
        r'^repolocation/detail/(?P<pk>[0-9]+)$',
        views.RepoLocationDetailView.as_view(),
        name='repolocation_detail'
    ),
    url(
        r'^repolocation/create/$',
        views.RepoLocationCreate.as_view(),
        name='repolocation_create'
    ),
    url(
        r'^repolocation/edit/(?P<pk>[0-9]+)$',
        views.RepoLocationUpdate.as_view(),
        name='repolocation_edit'
    ),
    url(
        r'^repolocation/delete/(?P<pk>[0-9]+)$',
        views.RepoLocationDelete.as_view(),
        name='repolocation_delete'),
]
