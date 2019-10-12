from django.urls import include, path
from . import views

app_name = "calheatmap"

urlpatterns = [
    path(
        'data/<app_name>/<model_name>/<field_name>',
        views.calheatmap_data,
        name='calheatmap_data'),
]
