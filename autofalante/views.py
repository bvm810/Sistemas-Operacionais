"""
Funções que chamam as páginas HTMLs a serem carregadas
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Playlist, Musica

COMMANDS_PLAYLIST_ID = 6
LOAD_ARDUINO_ID = 9992

def index(request):
    musicas = Musica.objects.exclude(playlist = COMMANDS_PLAYLIST_ID)
    songs = []
    for musica in musicas:
        if (Musica.objects.filter(arduino_id = musica.arduino_id).count()==1):
            s = Musica.objects.get(arduino_id = musica.arduino_id)
            songs.append(s)
        else:
            s = Musica.objects.filter(arduino_id = musica.arduino_id)[0]
            if (s.arduino_id != songs[len(songs)-1].arduino_id):
                songs.append(s)            
    template = loader.get_template('autofalante/index.html')
    context = {
        'songs': songs,
    }
    return render(request,'autofalante/index.html',context)

def home(request):
    created_playlists = Playlist.objects.exclude(id = COMMANDS_PLAYLIST_ID)
    musicas = Musica.objects.exclude(playlist = COMMANDS_PLAYLIST_ID)
    songs = []
    for musica in musicas:
        if (Musica.objects.filter(arduino_id = musica.arduino_id).count()==1):
            s = Musica.objects.get(arduino_id = musica.arduino_id)
            songs.append(s)
        else:
            s = Musica.objects.filter(arduino_id = musica.arduino_id)[0]
            if (s.arduino_id != songs[len(songs)-1].arduino_id):
                songs.append(s)            
    template = loader.get_template('autofalante/home.html')
    context = {
        'created_playlists': created_playlists,
        'songs': songs,
    }
    return render(request,'autofalante/home.html',context)

def detail(request, playlist_id, load):
    playlist = Playlist.objects.get(id = playlist_id)
    musicas_playlist = playlist.musica_set.all()
    fila = Musica.objects.all()
    if (load == 1):
        song = musicas_playlist[0]
        song.execute = True
        song.save()
        for m in fila:
            m.in_line = False
            m.save()
        comando = Musica.objects.get(arduino_id = 9993)
        comando.execute = True
        comando.save()
        for musica in musicas_playlist[1:]:
            musica.in_line = True
            musica.save()
    template = loader.get_template('autofalante/detail.html')
    context = {
        'musicas_playlist': musicas_playlist,
        'playlist': playlist,
    }
    return render(request,'autofalante/detail.html',context)

def sendCommand(request, playlist_id, musica_arduino_id):
    m = Musica.objects.filter(arduino_id = musica_arduino_id)
    musica = m[0]
    if (musica.execute == False):
        musica.execute = True
        musica.save()
    if (playlist_id == 0):
        return home(request)
    else:    
        return detail(request,playlist_id,0)

def sendLineIndex(request, musica_arduino_id):
    comando = Musica.objects.get(arduino_id = 9992)
    if (comando.execute == False):
        comando.execute = True
        comando.save()
    m = Musica.objects.filter(arduino_id = musica_arduino_id)
    musica = m[0]
    if (musica.in_line == False):
        musica.in_line = True
        musica.save()
    return index(request)

def sendLineHome(request, playlist_id, musica_arduino_id):
    comando = Musica.objects.get(arduino_id = 9992)
    if (comando.execute == False):
        comando.execute = True
        comando.save()
    m = Musica.objects.filter(arduino_id = musica_arduino_id)
    musica = m[0]
    if (musica.in_line == False):
        musica.in_line = True
        musica.save()
    if (playlist_id == 0):
        return home(request)
    else:    
        return detail(request,playlist_id,0)        

def getCommand(request):
    musica_line = Musica.objects.filter(execute = True).order_by('modified_at')
    template = loader.get_template('autofalante/esp.html')
    for musica in musica_line:
        musica.execute = False
        musica.save()
    context = {'musica_line': musica_line}
    return render(request,'autofalante/esp.html',context)

def getLine(request):
    musica_line = Musica.objects.filter(in_line = True).order_by('modified_at')[:100]
    template = loader.get_template('autofalante/esp.html')
    for musica in musica_line:
        musica.in_line = False
        musica.save()
    context = {'musica_line': musica_line}
    return render(request,'autofalante/esp.html',context)
