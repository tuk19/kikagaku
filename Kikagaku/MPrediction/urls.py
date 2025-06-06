from django.urls import path 
from MPrediction import views

app_name = 'mprediction'

urlpatterns = [
    path('', views.index, name='index')
]
