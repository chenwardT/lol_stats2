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

@admin.register(MatchDetail)
class MatchDetailAdmin(admin.ModelAdmin):
    list_display = ('region', 'match_id', 'queue_type', 'match_date', 'match_version')