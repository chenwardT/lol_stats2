from rest_framework import serializers

from .models import League, LeagueEntry


class LeagueEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueEntry
        fields = ('division', 'is_fresh_blood', 'is_hot_streak', 'is_inactive',
                  'is_veteran', 'league_points', 'player_or_team_id',
                  'player_or_team_name', 'wins', 'losses', 'series_losses',
                  'series_progress', 'series_target', 'series_wins')


class LeagueSerializer(serializers.ModelSerializer):
    leagueentry_set = LeagueEntrySerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ('region', 'queue', 'name', 'tier', 'leagueentry_set')
