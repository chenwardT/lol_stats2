from django.contrib import admin

from .models import Summoner

@admin.register(Summoner)
class SummonerAdmin(admin.ModelAdmin):
    pass