from rest_framework import serializers
from . models import ArchResource


class ArchResourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ArchResource
        exclude = ['creators']
