from django.conf.urls import url
from . import dal_views

app_name = 'archiv'

urlpatterns = [
    url(
        r'^archresource-autocomplete/$', dal_views.ArchResourceAC.as_view(),
        name='archresource-autocomplete',
    ),
]
