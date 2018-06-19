"""
Arquivo com os modelos de dados usandos no BD
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Playlist(models.Model):
	#Classe contendo modelo para a playlist com título e data 
	#de criação
	playlist_title = models.CharField('nome', max_length = 200)
	creation_date = models.DateTimeField('data de criação')
	creator = models.ForeignKey(User, on_delete = models.CASCADE)
	def __str__(self):
		return self.playlist_title

class Musica(models.Model):
	#Classe contendo o modelo para a música com playlist-pai, 
	#número de identificação no Arduino, título da música,
	#intérprete e álbum
	playlist = models.ForeignKey(Playlist, on_delete = models.CASCADE)
	execute = models.BooleanField('Execução foi pedida', editable = True)
	in_line = models.BooleanField('Na fila de execução', editable = True)
	modified_at = models.DateTimeField('data de modificação', auto_now = True)
	creation_date = models.DateTimeField('data de criação', default = timezone.now())
	arduino_id = models.IntegerField('ID no Arduino')
	song_title = models.CharField('título', max_length = 200)
	song_interpret = models.CharField('intérprete', max_length = 200)
	song_album = models.CharField('álbum', max_length = 200)	
	def __str__(self):
		return self.song_title

class Listener(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	playlists = models.ManyToManyField(Playlist)


