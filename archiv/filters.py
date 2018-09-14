import django_filters
from django import forms

from vocabs.models import SkosConcept
from . models import ArchResource


class ArchResourceListFilter(django_filters.FilterSet):
    res_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="res_type"
        ),
        help_text=ArchResource._meta.get_field('res_type').help_text,
        label=ArchResource._meta.get_field('res_type').verbose_name
        )

    class Meta:
        model = ArchResource
        fields = "__all__"
