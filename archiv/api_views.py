from rest_framework import viewsets
from rest_framework.settings import api_settings

from . models import ArchResource
from . api_renderers import ArchresTeiRenderer
from . serializers import ArchResourceSerializer


class ArchResourceViewSet(viewsets.ModelViewSet):
    queryset = ArchResource.objects.all()
    serializer_class = ArchResourceSerializer

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (ArchresTeiRenderer,)
