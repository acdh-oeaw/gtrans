from django.urls import include, path
from . import views

app_name = "netviz"

urlpatterns = [
    path('graph/<app_name>/<model_name>/<pk>', views.graph_data, name='graph'),
    path('graph/<app_name>/<model_name>', views.qs_graph_data, name='qs_as_graph'),
]
