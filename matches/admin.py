from django.contrib import admin

from .models import (MatchDetail,
                     Participant,
                     ParticipantIdentity,
                     Team,
                     Timeline,
                     Mastery,
                     ParticipantTimeline,
                     Rune,
                     BannedChampion,
                     Frame,
                     Event,
                     ParticipantFrame,
                     Position)

class ParticipantInline(admin.TabularInline):
    model = Participant

class ParticipantIdentityInline(admin.TabularInline):
    model = ParticipantIdentity

class TeamInline(admin.TabularInline):
    model = Team

@admin.register(MatchDetail)
class MatchDetailAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'region', 'queue_type', 'match_date', 'match_version')

    inlines = [
        ParticipantInline,
        ParticipantIdentityInline,
        TeamInline,
    ]