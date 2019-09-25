from django.urls import include, path
from . import views

app_name = "netviz"

urlpatterns = [
    path('graph/<app_name>/<model_name>/<pk>', views.graph_data, name='graph'),
]
