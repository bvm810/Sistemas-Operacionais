from django import forms
from django.core.exceptions import ValidationError
from .models import Playlist, Musica, Listener
from django.contrib.auth.models import User

class PlaylistCreationForm(forms.Form):
	playlist_name = forms.CharField(label = 'Título', max_length = 200)

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']

		if (Playlist.objects.filter(playlist_title = data).count()>0):
			raise ValidationError('Playlist já existente')

		return data


class PlaylistDeletionForm(forms.Form):
	playlist_name = forms.CharField(label = 'Título', max_length = 200)
	username = forms.CharField(max_length = 200, widget = forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(PlaylistDeletionForm, self).__init__(*args,**kwargs)
		self.fields['username'].initial = self.request.user.username 

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']
		user = self.fields['username'].initial
		print(user)

		if (Playlist.objects.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist inexistente')

		if(User.objects.get(username = user).listener.playlists.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist não pertence ao usuário')

		return data		