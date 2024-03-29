from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from archiv.api_views import ArchResourceViewSet
from entities.api_views import *
from vocabs import api_views

router = routers.DefaultRouter()
router.register(r'geojson', GeoJsonViewSet, basename='places')
router.register(r'skoslabels', api_views.SkosLabelViewSet)
router.register(r'skosnamespaces', api_views.SkosNamespaceViewSet)
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)
router.register(r'archresource', ArchResourceViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'institutions', InstitutionViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^netviz/', include('netviz.urls', namespace="netviz")),
    url(r'^wordcloud/', include('wordcloud.urls', namespace="wordcloud")),
    url(r'^calheatmap/', include('calheatmap.urls', namespace="calheatmap")),
    url(r'^admin/', admin.site.urls),
    url(r'^archiv/', include('archiv.urls', namespace='archiv')),
    url(r'^archiv-ac/', include('archiv.dal_urls', namespace='archiv-ac')),
    url(r'^vocabs/', include('vocabs.urls', namespace='vocabs')),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(r'^entities/', include('entities.urls', namespace='entities')),
    url(r'^entities-ac/', include('entities.dal_urls', namespace='entities-ac')),
    url(r'^charts/', include('charts.urls', namespace='charts')),
    url(r'^search/', include('haystack.urls')),
    url(r'^transkribus/', include('transkribus.urls', namespace='transkribus')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]
