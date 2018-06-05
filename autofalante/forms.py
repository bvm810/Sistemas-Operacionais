from django import forms
from django.core.exceptions import ValidationError
from .models import Playlist

class PlaylistCreationForm(forms.Form):
	playlist_name = forms.CharField(label = 'Título', max_length = 200)

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']

		if (Playlist.objects.filter(playlist_title = data).count()>0):
			raise ValidationError('Playlist já existente')

		return data


class PlaylistDeletionForm(forms.Form):
	playlist_name = forms.CharField(label = 'Título', max_length = 200)

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']

		if (Playlist.objects.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist inexistente')

		return data		