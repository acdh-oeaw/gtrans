import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from . utils import as_graph, qs_as_graph


def graph_data(request, app_name, model_name, pk):
    try:
        ct = ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        return JsonResponse({})
    try:
        int_pk = int(pk)
    except ValueError:
        return JsonResponse({})
    res = ct.model_class().objects.get(id=int_pk)
    graph = as_graph(res)
    return JsonResponse(graph)


def qs_graph_data(request, app_name, model_name):
    try:
        ct = ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        return JsonResponse({})
    qs = ct.model_class().objects.all()
    graph = qs_as_graph(qs)
    return JsonResponse(graph)
