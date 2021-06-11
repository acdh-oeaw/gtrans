from django.conf.urls import url
from . import views
from . import tei_views

from archeutils import views as arche_views


app_name = 'archiv'

urlpatterns = [
    url(
        r'^ids$',
        arche_views.get_ids,
        name='get_ids'
    ),
    url(
        r'^archresource/arche/(?P<pk>[0-9]+)$',
        arche_views.res_as_arche_graph,
        name='arche_res'
    ),
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
    url(
        r'^archresource/xml-tei/(?P<pk>[0-9]+)$',
        tei_views.archres_as_tei,
        name='archresource_xml'
    ),
]
