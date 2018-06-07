"""
Arquivo que diz como e quais classes serão mostradas no
lado admin do site
"""

from django.contrib import admin
from .models import Musica, Playlist, Listener
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

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

class PlaylistInline(admin.TabularInline):
	model = Playlist
	extra = 1

class ListenerInline(admin.StackedInline):
	model = Listener
	can_delete = False
	verbose_name_plural = 'ouvintes'

class UserAdmin(BaseUserAdmin):
	inlines = (ListenerInline, PlaylistInline, ) 


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Playlist,PlaylistAdmin)
