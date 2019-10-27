from rest_framework import viewsets

from . models import ArchResource
from . serializers import ArchResourceSerializer


class ArchResourceViewSet(viewsets.ModelViewSet):
    queryset = ArchResource.objects.all()
    serializer_class = ArchResourceSerializer
