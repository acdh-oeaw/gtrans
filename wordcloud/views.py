import json
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType


def word_data_class(request, app_name, model_name, field_name):
    try:
        ct = ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        return JsonResponse({})
    my_model_class = ct.model_class()
    items = list(my_model_class.objects.all().values(field_name))
    text = Counter(" ".join([x[field_name] for x in items]).split(' '))
    data = [
        {'name': x[0], 'weight': x[1]} for x in text.items()
    ]
    return JsonResponse(data, safe=False)


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
