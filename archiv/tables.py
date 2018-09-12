import django_tables2 as tables
from django_tables2.utils import A
from entities.models import *
from archiv.models import *


class ArchResourceTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:archresource_detail',
        args=[A('pk')], verbose_name='ID'
    )
    title = tables.LinkColumn(
        'archiv:archresource_detail',
        args=[A('pk')], verbose_name='Titel'
    )
    mentioned_person = tables.ManyToManyColumn()
    mentioned_inst = tables.ManyToManyColumn()
    mentioned_place = tables.ManyToManyColumn()
    creator_person = tables.ManyToManyColumn()
    creator_inst = tables.ManyToManyColumn()
    forename = tables.Column()

    class Meta:
        model = ArchResource
        sequence = ('id', 'title',)
        attrs = {"class": "table table-responsive table-hover"}


class RepoLocationTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:repolocation_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'archiv:repolocation_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = RepoLocation
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}
