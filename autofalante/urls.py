from django.urls import path
from . import views

app_name = 'autofalante'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:playlist_id>/<int:load>/', views.detail, name='detail'),
    path('fila/<int:playlist_id>/<int:musica_arduino_id>/', views.sendLine, name='sendLine'),
    path('comandos/<int:playlist_id>/<int:musica_arduino_id>/', views.sendCommand, name='sendCommand'),
    path('esp/fila/', views.getLine, name='getLine'),
    path('esp/comandos/', views.getCommand, name='getCommand'),
]