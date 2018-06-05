from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'autofalante'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.login, {'template_name': 'autofalante/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/autofalante'}, name='logout'),
    path('home/', views.home, name='home'),
    path('home/<int:playlist_id>/<int:load>/', views.detail, name='detail'),
    path('home/fila/<int:playlist_id>/<int:musica_arduino_id>/', views.sendLineHome, name='sendLineHome'),
    path('home/add/<int:playlist_id>/<int:musica_arduino_id>/', views.addSongPlaylist, name='addSongPlaylist'),
    path('home/remove/<int:playlist_id>/<int:musica_arduino_id>/', views.removeSongPlaylist, name='removeSongPlaylist'),
    path('fila/<int:musica_arduino_id>/', views.sendLineIndex, name='sendLineIndex'),
    path('home/comandos/<int:playlist_id>/<int:musica_arduino_id>/', views.sendCommand, name='sendCommand'),
    path('esp/fila/', views.getLine, name='getLine'),
    path('esp/comandos/', views.getCommand, name='getCommand'),
]