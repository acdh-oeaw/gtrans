from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import PlaceSerializer, GeoJsonSerializer
from .models import Place
from .api_renderers import GeoJsonRenderer
from rest_framework.settings import api_settings


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    depth = 2


class GeoJsonViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Place.objects.all()
        serializer = GeoJsonSerializer(queryset, many=True)
        return Response(serializer.data)

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (GeoJsonRenderer,)
