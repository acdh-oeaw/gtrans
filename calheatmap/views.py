import collections

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from . utils import vis_date_utc


def calheatmap_data(request, app_name, model_name, field_name):
    try:
        ct = ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        return JsonResponse({})
    model = ct.model_class()
    qs = model.objects.all()
    to_exlcude = {
        field_name: None
    }
    qs = model.objects.exclude(**to_exlcude)
    my_data = collections.Counter([f"{vis_date_utc(x, field_name)}" for x in qs])
    return JsonResponse(my_data, safe=True)
