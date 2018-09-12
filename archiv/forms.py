from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *

from .models import RepoLocation, ArchResource


class RepoLocationForm(forms.ModelForm):
    class Meta:
        model = RepoLocation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RepoLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ArchResourceForm(forms.ModelForm):
    class Meta:
        model = ArchResource
        fields = "__all__"
        widgets = {
            'res_type': autocomplete.ModelSelect2(
                url='../../../vocabs-ac/skos-constraint-ac/?scheme=res_type'),
            'subject_norm': autocomplete.ModelSelect2Multiple(
                url='../../../vocabs-ac/skos-constraint-ac/?scheme=subject_norm'),
            'creator_inst': autocomplete.ModelSelect2Multiple(
                url='entities-ac:institution-autocomplete'),
            'creator_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'),
            'mentioned_inst': autocomplete.ModelSelect2Multiple(
                url='entities-ac:institution-autocomplete'),
            'mentioned_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(ArchResourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class GenericFilterFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))


class ArchResourceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ArchResourceFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'title',
                    'res_type',
                    css_id="basic_search_fields"
                    ),
                AccordionGroup(
                    'Inhalt',
                    'subject_norm',
                    'subject_free',
                    'abstract',
                    css_id="more"
                    ),
                AccordionGroup(
                    'Datierung',
                    'written_date',
                    'not_before',
                    'not_after',
                    css_id="datierung"
                    ),
                AccordionGroup(
                    'Bestand',
                    'location',
                    'location__archiv',
                    css_id="bestand"
                    ),
                )
            )


class RepoLocationFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RepoLocationFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'name',
                    css_id="basic_search_fields"
                    ),
                )
            )


class PersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'name',
                    'written_name',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search',
                    'acad_title',
                    'alt_names',
                    'authority_url',
                    'belongs_to_institution',
                    css_id="more"
                    ),
                )
            )


class AlternativeNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AlternativeNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'name',
                    css_id="basic_search_fields"
                    ),
                )
            )


class InstitutionFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InstitutionFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'written_name',
                    'alt_names',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search'
                    'authority_url',
                    'location',
                    css_id="more"
                    ),
                )
            )


class PlaceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlaceFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'name',
                    'alternative_name',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search'
                    'geonames_id',
                    'part_of',
                    css_id="more"
                    ),
                )
            )
