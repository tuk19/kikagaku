from django.urls import path 
from MPrediction import views

app_name = 'mprediction'

urlpatterns = [
    path('', views.index, name='index'),
    path('team/', views.team, name='team'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/edit/<int:num>', views.team_edit, name='team_edit'),
    path('player/', views.player, name='player'),
    path('player/create/', views.player_create, name='player_create'),
    path('player/edit/<int:num>', views.player_edit, name='player_edit'),
    path('member/', views.member, name='member'),
    path('member/create/', views.member_create, name='member_create'),
    path('member/edit/<int:num>', views.member_edit, name='member_edit'),
    path('season/', views.season, name='season'),
    path('season/create/', views.season_create, name='season_create'),
    path('season/edit/<int:num>', views.season_edit, name='season_edit'),
]
