"""
Arquivo que diz como e quais classes serão mostradas no
lado admin do site
"""

from django.contrib import admin
from .models import Musica, Playlist

class SongInline(admin.TabularInline):
	model = Musica
	extra = 1

class PlaylistAdmin(admin.ModelAdmin):
	fieldsets = [
		('INFORMAÇÕES GERAIS', {'fields': ['playlist_title', 'creation_date']}),
	]
	inlines = [SongInline]
	list_display = ('playlist_title', 'creation_date')
	list_filter = ['creation_date']
	search_fields = ['playlist_title']

admin.site.register(Playlist,PlaylistAdmin)
