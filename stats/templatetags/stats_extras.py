from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def create_object_count(app=None):

    """fetches all models of the passed in app and returns a
    dict containg the name of each class and the number of instances"""

    if app:
        models = ContentType.objects.filter(app_label=app)
        result = []
        for x in models:
            model = x.model_class()
            try:
                item = {
                    'name': model._meta.verbose_name.title(),
                    'count': model.objects.count()
                }
            except Exception as e:
                item = {
                    'name': x,
                    'count': e
                }
                model = None
                item['link'] = None
            try:
                item['link'] = model.get_listview_url()
            except AttributeError:
                item['link'] = None
            result.append(item)
        return result

    else:
        result = [
            {
                'name': 'no parameter passed in',
                'count': '1'
            }
        ]
        return result
