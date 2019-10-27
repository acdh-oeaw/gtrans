from rest_framework import serializers
from . models import ArchResource
from entities.serializers import *
from vocabs.serializers import *


class ArchResourceSerializer(serializers.HyperlinkedModelSerializer):

    mentioned_person = PersonSerializer(many=True, read_only=True)
    mentioned_inst = InstitutionSerializer(many=True, read_only=True)
    mentioned_place = PlaceSerializer(many=True, read_only=True)
    subject_norm = SkosConceptSerializer(many=True, read_only=True)
    tei_doc = serializers.SerializerMethodField()

    class Meta:
        model = ArchResource
        exclude = ['creators', ]

    def get_tei_doc(self, obj):
        return obj.as_tei()
