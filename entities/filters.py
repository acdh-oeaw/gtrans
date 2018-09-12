import django_filters
from django import forms

from . models import Person, Place, Institution


class PersonListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Person._meta.get_field('name').help_text,
        label=Person._meta.get_field('name').verbose_name
        )
    belongs_to_institution = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(),
        help_text=Person._meta.get_field('belongs_to_institution').help_text,
        label=Person._meta.get_field('belongs_to_institution').verbose_name
        )

    class Meta:
        model = Person
        fields = "__all__"


class PlaceListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Place._meta.get_field('name').help_text,
        label=Place._meta.get_field('name').verbose_name
        )

    class Meta:
        model = Place
        fields = "__all__"


class InstitutionListFilter(django_filters.FilterSet):
    written_name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Institution._meta.get_field('written_name').help_text,
        label=Institution._meta.get_field('written_name').verbose_name
        )

    class Meta:
        model = Institution
        fields = "__all__"
