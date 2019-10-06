import json
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType


def word_data(request, app_name, model_name, pk, field_name):
    try:
        ct = ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        return JsonResponse({})
    try:
        int_pk = int(pk)
    except ValueError:
        return JsonResponse({})
    res = ct.model_class().objects.get(id=int_pk)
    text = getattr(res, 'abstract')
    splitted = text.replace('.', ' ').replace(',', '').split(' ')
    data = [
        {'name': x[0], 'weight': x[1]} for x in Counter(splitted).items()
    ]
    return JsonResponse(data, safe=False)
