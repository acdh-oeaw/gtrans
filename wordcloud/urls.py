from django.urls import include, path
from . import views

app_name = "wordcloud"

urlpatterns = [
    path('all-words/<app_name>/<model_name>/<field_name>', views.word_data_class, name='all_words'),
    path('words/<app_name>/<model_name>/<pk>/<field_name>', views.word_data, name='words'),
]
