from django.urls import path
from DogPose import views

app_name = 'dogpose'

urlpatterns = [
    path('', views.index, name='index')
]
