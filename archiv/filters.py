import django_filters

from dal import autocomplete
from django import forms
from django.contrib.auth.models import User

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution, Person, Place
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
    mentioned_person = django_filters.ModelMultipleChoiceFilter(
        queryset=Person.objects.all(),
        help_text=ArchResource._meta.get_field('mentioned_person').help_text,
        label=ArchResource._meta.get_field('mentioned_person').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="entities-ac:person-autocomplete",
        )
    )
    creator_person = django_filters.ModelMultipleChoiceFilter(
        queryset=Person.objects.exclude(created_by_person=None),
        help_text=ArchResource._meta.get_field('creator_person').help_text,
        label=ArchResource._meta.get_field('creator_person').verbose_name,
        # widget=autocomplete.Select2Multiple(
        #     url="entities-ac:person-autocomplete",
        # )
    )
    mentioned_inst = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(),
        help_text=ArchResource._meta.get_field('mentioned_inst').help_text,
        label=ArchResource._meta.get_field('mentioned_inst').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="entities-ac:institution-autocomplete",
        )
    )
    creator_inst = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.exclude(created_by_inst=None),
        help_text=ArchResource._meta.get_field('creator_inst').help_text,
        label=ArchResource._meta.get_field('creator_inst').verbose_name,
        # widget=autocomplete.Select2Multiple(
        #     url="entities-ac:institution-autocomplete",
        # )
    )
    mentioned_place = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.objects.all(),
        help_text=ArchResource._meta.get_field('mentioned_place').help_text,
        label=ArchResource._meta.get_field('mentioned_place').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="entities-ac:place-autocomplete",
        )
    )
    creators = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        help_text=ArchResource._meta.get_field('creators').help_text,
        label=ArchResource._meta.get_field('creators').verbose_name
    )

    class Meta:
        model = ArchResource
        fields = "__all__"
