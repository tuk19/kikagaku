from django.urls import path
from MusicClassification import views

app_name = 'musicclassification'

urlpatterns = [
    path('', views.index, name='index'),
]
