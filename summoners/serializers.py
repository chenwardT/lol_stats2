from rest_framework import serializers

from .models import Summoner


class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = ('summoner_id', 'region', 'name', 'summoner_level', 'last_update')
