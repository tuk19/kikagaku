from django.urls import path
from MusicGeneration import views

app_name = 'musicgeneration'

urlpatterns = [
    path('', views.index, name='index'),
]