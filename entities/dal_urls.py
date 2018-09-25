from django.conf.urls import url
from . import views
from . import dal_views
from .models import *

app_name = 'vocabs'

urlpatterns = [
    url(
        r'^place-autocomplete/$', dal_views.PlaceAC.as_view(
            model=Place),
        name='place-autocomplete',
    ),
    url(
        r'^person-autocomplete/$', dal_views.PersonAC.as_view(
            model=Person),
        name='person-autocomplete',
    ),
    url(
        r'^institution-autocomplete/$', dal_views.InstitutionAC.as_view(
            model=Institution),
        name='institution-autocomplete',
    ),
]
