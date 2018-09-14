import django_filters

from dal import autocomplete
from django import forms

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution
from . models import ArchResource


class ArchResourceListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ArchResource._meta.get_field('title').help_text,
        label=ArchResource._meta.get_field('title').verbose_name
    )
    signature = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ArchResource._meta.get_field('signature').help_text,
        label=ArchResource._meta.get_field('signature').verbose_name
    )
    abstract = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ArchResource._meta.get_field('abstract').help_text,
        label=ArchResource._meta.get_field('abstract').verbose_name
    )
    archiv = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.filter(
            institution_type="Archiv"
        ),
        help_text=ArchResource._meta.get_field('archiv').help_text,
        label=ArchResource._meta.get_field('archiv').verbose_name,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'chbx-select-multi'})
    )
    res_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="res_type"
        ),
        help_text=ArchResource._meta.get_field('res_type').help_text,
        label=ArchResource._meta.get_field('res_type').verbose_name,
        method=generous_concept_filter,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'chbx-select-multi'})
    )
    subject_norm = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="schlagwort"
        ),
        help_text=ArchResource._meta.get_field('subject_norm').help_text,
        label=ArchResource._meta.get_field('subject_norm').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/current-land-use",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
    )

    class Meta:
        model = ArchResource
        fields = "__all__"
