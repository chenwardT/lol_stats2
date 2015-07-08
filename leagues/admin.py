from django.contrib import admin

from .models import League, LeagueEntry

class LeagueEntryInline(admin.TabularInline):
    model = LeagueEntry

    ordering = ('-league_points',)

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'queue', 'region')

    inlines = [
        LeagueEntryInline,
    ]

    list_filter = ('region', 'queue', 'tier')