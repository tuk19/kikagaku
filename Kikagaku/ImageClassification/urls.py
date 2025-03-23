from django.urls import path
from ImageClassification import views

app_name = 'imageclassification'

urlpatterns = [
    path('', views.index, name='index')
]
