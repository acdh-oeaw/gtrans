import json
from rest_framework import serializers
from .models import Place


class GeoJsonSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        if obj.lng:
            geojson = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(obj.lng), float(obj.lat)]
                    },
                "properties": {
                    "name": obj.name,
                    "placeType": obj.place_type
                }
            }
            return geojson
        else:
            return None


class PlaceHelperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    part_of = PlaceHelperSerializer(many=False)

    class Meta:
        model = Place
        fields = "__all__"
