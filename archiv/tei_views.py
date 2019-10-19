from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from . models import ArchResource


def archres_as_tei(request, pk):
    obj = get_object_or_404(ArchResource, pk=pk)
    mytei = obj.as_tei()
    return HttpResponse(mytei, content_type="text/xml")
