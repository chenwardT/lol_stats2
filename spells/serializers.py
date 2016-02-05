from rest_framework import serializers

from .models import SummonerSpell

class SummonerSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonerSpell
