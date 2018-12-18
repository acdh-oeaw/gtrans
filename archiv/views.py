import pandas as pd
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from reversion.models import Version

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from vocabs.models import SkosConceptScheme, SkosConcept
from . filters import *
from . forms import *
from . tables import *
from . models import ArchResource


class SchlagwortList(tables.SingleTableView):
    paginate_by = 25
    template_name = 'archiv/schlagwort_list.html'
    model = SkosConcept

    def get_queryset(self, **kwargs):
        qs = super(SchlagwortList, self).get_queryset()
        selected_scheme = SkosConceptScheme.objects.filter(dc_title__icontains='schlagwort')
        qs = self.model.objects.filter(scheme__in=selected_scheme)
        return qs

    def get_table(self, **kwargs):
        table = super(SchlagwortList, self).get_table()
        concepts = self.get_queryset()
        col_headers = ['id', '1. Ebene', '2. Ebene', '3. Ebene', 'Synonyme', 'Dokumente']
        row = []
        for x in concepts:
            temp_row = {}
            docs = ArchResource.objects.filter(subject_norm=x).count()
            if getattr(x.broader_concept, 'broader_concept', None):
                labels = " | ".join(y.label for y in x.other_label.all())
                temp_row = {
                    'id': x.id,
                    'first': x.broader_concept.broader_concept,
                    'second': x.broader_concept,
                    'third': x,
                    'syns': labels,
                }
            elif getattr(x, 'broader_concept', None):
                temp_row = {
                    'id': x.id,
                    'first': x.broader_concept,
                    'second': x,
                    'third': None,
                    'syns': None,
                }
            else:
                temp_row = {
                    'id': x.id,
                    'first': x,
                    'second': None,
                    'third': None,
                    'syns': None,
                }
            temp_row['docs'] = docs
            row.append(temp_row)

            class MyTable(tables.Table):
                id = tables.TemplateColumn(
                    """
        <a
            href="{% url 'archiv:archresource_browse' %}?subject_norm={{ record.id }}&Filter=Search"
            target="_blank">
            {{ record.id }} <i class="fas fa-external-link-alt"></i>
        </a>
                    """
                )
                first = tables.Column()
                second = tables.Column()
                third = tables.Column()
                syns = tables.Column()
                docs = tables.Column()

                class Meta:
                    attrs = {"class": "table table-responsive table-hover"}

            table = MyTable(row)
            RequestConfig(self.request, paginate={'per_page': concepts.count()}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(SchlagwortList, self).get_context_data()
        return context


class ArchResourceListView(GenericListView):
    model = ArchResource
    filter_class = ArchResourceListFilter
    formhelper_class = ArchResourceFilterFormHelper
    table_class = ArchResourceTable
    init_columns = [
        'id',
        'title',
        'signature',
    ]


class ArchResourceDetailView(DetailView):
    model = ArchResource
    template_name = 'archiv/archres_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArchResourceDetailView, self).get_context_data()
        context['history'] = Version.objects.get_for_object(self.object)
        return context


class ArchResourceCreate(BaseCreateView):

    model = ArchResource
    form_class = ArchResourceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchResourceCreate, self).dispatch(*args, **kwargs)


class ArchResourceUpdate(BaseUpdateView):

    model = ArchResource
    form_class = ArchResourceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchResourceUpdate, self).dispatch(*args, **kwargs)


class ArchResourceDelete(DeleteView):
    model = ArchResource
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('archiv:archresource_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchResourceDelete, self).dispatch(*args, **kwargs)
