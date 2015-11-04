from django.contrib import admin

from .models import Summoner
from matches.models import ParticipantIdentity


class ParticipantIdentityInline(admin.TabularInline):
    model = ParticipantIdentity


@admin.register(Summoner)
class SummonerAdmin(admin.ModelAdmin):
    list_display = ('summoner_id', 'region', 'name', 'last_update')

    list_filter = ('region',)

    # FIXME: Very slow.
    # inlines = [
    #     ParticipantIdentityInline,
    # ]