from django.urls import path
from PoseAnalysis import views

app_name = 'poseanalysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<str:filename>/', views.download_video, name='download_video'),
]
