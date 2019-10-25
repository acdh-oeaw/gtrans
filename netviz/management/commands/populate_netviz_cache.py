import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


from netviz.models import NetVisCache
from netviz.utils import qs_as_graph


class Command(BaseCommand):

    help = "Populate the netviz cache"

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name', type=str,
            help="Name of the app for which you'd like to populate the cache."
        )
        parser.add_argument(
            'model_name', type=str,
            help="Name of the model for which  you'd like to populate the cache."
        )

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        model_name = kwargs['model_name']
        try:
            ct = ContentType.objects.get(app_label=app_name, model=model_name)
        except ObjectDoesNotExist:
            return f"A model: {model_name} in app: {app_name} could not be found"
        qs = ct.model_class().objects.all()
        limit = len(qs)
        graph = qs_as_graph(qs, limit=limit)
        netvis_cache, _ = NetVisCache.objects.get_or_create(
            app_name=app_name,
            model_name=model_name
        )
        netvis_cache.graph_data = json.dumps(graph)
        netvis_cache.save()
        return "done"
