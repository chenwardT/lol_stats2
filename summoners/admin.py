from django.contrib import admin

from .models import Summoner

@admin.register(Summoner)
class SummonerAdmin(admin.ModelAdmin):
    list_display = ('summoner_id', 'region', 'name', 'last_update')