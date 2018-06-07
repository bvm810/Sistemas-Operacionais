from django import forms
from django.core.exceptions import ValidationError
from .models import Playlist, Musica, Listener
from django.contrib.auth.models import User

class PlaylistCreationForm(forms.Form):
	playlist_name = forms.CharField(label = 'Nome', max_length = 200)

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']

		if (Playlist.objects.filter(playlist_title = data).count()>0):
			raise ValidationError('Playlist já existente')

		return data


class PlaylistDeletionForm(forms.Form):
	playlist_name = forms.CharField(label = 'Nome', max_length = 200)
	username = forms.CharField(max_length = 200, widget = forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(PlaylistDeletionForm, self).__init__(*args,**kwargs)
		self.fields['username'].initial = self.request.user.username 

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']
		user = self.fields['username'].initial

		if(User.objects.get(username = user).listener.playlists.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist inexistente ou não disponível ao usuário')

		if(Playlist.objects.get(playlist_title = data).creator != User.objects.get(username = user)):
			raise ValidationError('Usuário não é o criador dessa playlist. Utilizar remoção')

		return data

class PlaylistSharingForm(forms.Form):
	playlist_name = forms.CharField(label = 'Playlist', max_length = 200)
	shared_user = forms.CharField(label = 'Usuário', max_length = 200)
	original_user = forms.CharField(max_length = 200, widget = forms.HiddenInput())		

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(PlaylistSharingForm, self).__init__(*args,**kwargs)
		self.fields['original_user'].initial = self.request.user.username

	def clean_shared_user(self):
		data = self.cleaned_data['shared_user']

		if(User.objects.filter(username = data).count()==0):
			raise ValidationError('Usuário inexistente')

		return data 

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']
		user = self.fields['original_user'].initial

		if(User.objects.get(username = user).listener.playlists.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist inexistente ou não disponível ao usuário')

		return data	

class PlaylistRemovalForm(forms.Form):
	playlist_name = forms.CharField(label = 'Nome', max_length = 200)
	username = forms.CharField(max_length = 200, widget = forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(PlaylistRemovalForm, self).__init__(*args,**kwargs)
		self.fields['username'].initial = self.request.user.username 

	def clean_playlist_name(self):
		data = self.cleaned_data['playlist_name']
		user = self.fields['username'].initial

		if(User.objects.get(username = user).listener.playlists.filter(playlist_title = data).count()==0):
			raise ValidationError('Playlist inexistente ou não disponível ao usuário')

		if(Playlist.objects.get(playlist_title = data).creator == User.objects.get(username = user)):
			raise ValidationError('Usuário é o criador dessa playlist. Apague a playlist')

		return data



