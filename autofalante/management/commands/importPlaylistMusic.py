from django.core.management.base import BaseCommand, CommandError
from autofalante.models import Playlist, Musica

ALL_SONGS_PLAYLIST_ID = 1
COMMANDS_PLAYLIST_ID = 6

class Command(BaseCommand):
	help = 'Coloca as músicas presentes nas playlists na playlist all.' 

	def handle(self, *args, **options):
		musicas = Musica.objects.exclude(playlist = COMMANDS_PLAYLIST_ID)
		songs = []
		for musica in musicas:
			if (Musica.objects.filter(arduino_id = musica.arduino_id).count()==1):
				s = Musica(
					playlist = Playlist.objects.get(id = ALL_SONGS_PLAYLIST_ID),
					execute = 0, 
					in_line = 0, 
					modified_at = musica.modified_at,
					arduino_id = musica.arduino_id,
					song_title = musica.song_title,
					song_interpret = musica.song_interpret,
					song_album = musica.song_album
					)
				songs.append(s)
				s.save()
			else:
				s = Musica.objects.filter(arduino_id = musica.arduino_id).order_by('modified_at').first()
				if (s.arduino_id != songs[len(songs)-1].arduino_id):
					songs.append(s)
					m = Musica(
						playlist = Playlist.objects.get(id = ALL_SONGS_PLAYLIST_ID),
						execute = 0, 
						in_line = 0, 
						modified_at = s.modified_at,
						arduino_id = s.arduino_id,
						song_title = s.song_title,
						song_interpret = s.song_interpret,
						song_album = s.song_album
						)
					m.save()	            	
