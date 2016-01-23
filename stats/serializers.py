from rest_framework.serializers import ModelSerializer

from champions.serializers import ChampionSerializer
from champions.models import Champion
from .models import ChampionStats, Bucket

class BucketSerializer(ModelSerializer):
    class Meta:
        model = Bucket

class ChampionStatsSerializer(ModelSerializer):
    bucket = BucketSerializer(read_only=True)
    champion = ChampionSerializer(read_only=True)

    class Meta:
        model = ChampionStats
        fields = ['avg_{}'.format(f) for f in Champion.aggregable_participant_fields] + ['champion', 'bucket']