from rest_framework import serializers

from .models import Champion


class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion
        fields = ('champion_id', 'name', 'title', 'key')
