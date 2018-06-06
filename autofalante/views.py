"""
Funções que chamam as páginas HTMLs a serem carregadas
"""

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Playlist, Musica, Listener
from .forms import PlaylistCreationForm, PlaylistDeletionForm, PlaylistSharingForm

COMMANDS_PLAYLIST_ID = 6
ALL_SONGS_PLAYLIST_ID = 1
LOAD_ARDUINO_ID = 9992

def index(request):
    songs = Musica.objects.filter(playlist = ALL_SONGS_PLAYLIST_ID)            
    template = loader.get_template('autofalante/index.html')
    context = {
        'songs': songs,
    }
    return render(request,'autofalante/index.html',context)

def home(request):
    if (request.user.is_authenticated):
        u = User.objects.get(username = request.user.username)
        owned_playlists = u.listener.playlists.all().order_by('playlist_title')
    else:
        owned_playlists = []    
    songs = Musica.objects.filter(playlist = ALL_SONGS_PLAYLIST_ID)
    if (request.method == 'POST' and 'create' in request.POST):
        creation_form = PlaylistCreationForm(request.POST)
        deletion_form = PlaylistDeletionForm(request = request)
        sharing_form = PlaylistSharingForm(request = request)
        if (creation_form.is_valid()):
            new_playlist = Playlist(
                playlist_title = creation_form.cleaned_data['playlist_name'],
                creation_date = timezone.now(),
            )    
            new_playlist.save()
            u.listener.playlists.add(new_playlist)
            creation_form = PlaylistCreationForm()
    elif(request.method == 'POST' and 'delete' in request.POST):    
        deletion_form = PlaylistDeletionForm(data = request.POST, request = request)
        creation_form = PlaylistCreationForm()
        sharing_form = PlaylistSharingForm(request = request)
        if (deletion_form.is_valid()):
            deleted_playlist = Playlist.objects.get(playlist_title = deletion_form.cleaned_data['playlist_name'])
            deleted_playlist.delete()
            deletion_form = PlaylistDeletionForm(request = request)
    elif(request.method == 'POST' and 'share' in request.POST):
        deletion_form = PlaylistDeletionForm(request = request)
        creation_form = PlaylistCreationForm()
        sharing_form = PlaylistSharingForm(data = request.POST, request = request)
        if(sharing_form.is_valid()):
            shared_playlist = Playlist.objects.get(playlist_title = sharing_form.cleaned_data['playlist_name'])
            shared_user = User.objects.get(username = sharing_form.cleaned_data['shared_user'])
            shared_user.listener.playlists.add(shared_playlist)
            sharing_form = PlaylistSharingForm(request = request)     
    else:
        creation_form = PlaylistCreationForm()
        deletion_form = PlaylistDeletionForm(request = request)
        sharing_form = PlaylistSharingForm(request = request)            
    template = loader.get_template('autofalante/home.html')
    context = {
        'owned_playlists': owned_playlists,
        'songs': songs,
        'creation_form': creation_form,
        'deletion_form': deletion_form,
        'sharing_form': sharing_form,
    }
    return render(request,'autofalante/home.html',context)

def detail(request, playlist_id, load):
    playlist = Playlist.objects.get(id = playlist_id)
    musicas_playlist = playlist.musica_set.all()
    fila = Musica.objects.all()
    if (load and musicas_playlist):
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
    other_songs = Musica.objects.filter(playlist = ALL_SONGS_PLAYLIST_ID)
    for s in musicas_playlist:
        other_songs = other_songs.exclude(arduino_id = s.arduino_id)                       
    template = loader.get_template('autofalante/detail.html')
    context = {
        'musicas_playlist': musicas_playlist,
        'playlist': playlist,
        'other_songs': other_songs,
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

def addSongPlaylist(request, playlist_id, musica_arduino_id):
    added_song = Musica.objects.filter(playlist = ALL_SONGS_PLAYLIST_ID).get(arduino_id = musica_arduino_id)
    s = Musica(
        playlist = Playlist.objects.get(id = playlist_id),
        execute = 0,
        in_line = 0,
        modified_at = added_song.modified_at,
        arduino_id = added_song.arduino_id,
        song_title = added_song.song_title,
        song_interpret = added_song.song_interpret,
        song_album = added_song.song_album 
        )
    s.save()
    return detail(request, playlist_id, 0)

def removeSongPlaylist(request, playlist_id, musica_arduino_id):
    removed_song = Musica.objects.filter(playlist = playlist_id).get(arduino_id = musica_arduino_id)
    removed_song.delete()
    return detail(request, playlist_id, 0)

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
