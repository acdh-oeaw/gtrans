from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse

from .utils import as_arche_graph, serialize_project, ARCHE_BASE_URL, get_arche_id

from archiv.models import ArchResource


def res_as_arche_graph(request, pk):
    format = request.GET.get('format', 'xml')
    try:
        res = ArchResource.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404(f"No object with id: {pk} found")
    g = as_arche_graph(res)
    if format == 'turtle':
        return HttpResponse(
            g.serialize(encoding='utf-8', format='turtle'), content_type='text/turtle'
        )
    else:
        return HttpResponse(
            g.serialize(encoding='utf-8'), content_type='application/xml'
        )


def project_as_arche_graph(request):
    g = serialize_project()
    if format == 'turtle':
        return HttpResponse(
            g.serialize(encoding='utf-8', format='turtle'), content_type='text/turtle'
        )
    else:
        return HttpResponse(
            g.serialize(encoding='utf-8'), content_type='application/xml'
        )


def get_ids(request):
    base_uri = request.build_absolute_uri().split('/archiv')[0]
    data = {
        "arche_constants": f"{base_uri}",
        "id_prefix": f"{ARCHE_BASE_URL}",
        "ids": [
            {
                "id": f"{get_arche_id(x)}",
                "filename": f"{slugify(x)}.xml",
                "md": f"{base_uri}{x.get_arche_url()}",
                "html": f"{base_uri}{x.get_absolute_url()}",
                "payload": f"{base_uri}{x.get_tei_url()}"
            } for x in ArchResource.objects.all()],
    }
    return JsonResponse(data)
