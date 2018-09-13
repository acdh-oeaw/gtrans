from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . filters import *
from . forms import *
from . tables import *
from . models import RepoLocation, ArchResource


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


class RepoLocationListView(GenericListView):
    model = RepoLocation
    filter_class = RepoLocationListFilter
    formhelper_class = RepoLocationFilterFormHelper
    table_class = RepoLocationTable
    init_columns = [
        'id',
    ]


class RepoLocationDetailView(DetailView):
    model = RepoLocation
    template_name = 'browsing/generic_detail.html'


class RepoLocationCreate(BaseCreateView):

    model = RepoLocation
    form_class = RepoLocationForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RepoLocationCreate, self).dispatch(*args, **kwargs)


class RepoLocationUpdate(BaseUpdateView):

    model = RepoLocation
    form_class = RepoLocationForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RepoLocationUpdate, self).dispatch(*args, **kwargs)


class RepoLocationDelete(DeleteView):
    model = RepoLocation
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('archiv:repolocation_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RepoLocationDelete, self).dispatch(*args, **kwargs)
