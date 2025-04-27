from django.urls import path
from ImageTranscription import views

app_name = 'imagetranscription'

urlpatterns = [
    path('', views.index, name='index'),
    path('image', views.image, name='image'),
    path('url', views.pdf, name='pdf')
]
