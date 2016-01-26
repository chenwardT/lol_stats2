from rest_framework.serializers import ModelSerializer, SerializerMethodField

from utils.constants import VALID_LANE_ROLE_COMBOS
from champions.models import Champion
from .models import ChampionStats


class ChampionStatsSerializer(ModelSerializer):
    name = SerializerMethodField()
    champion_id = SerializerMethodField()
    role = SerializerMethodField()

    def get_name(self, champion_stats):
        return champion_stats.champion.name

    def get_champion_id(self, champion_stats):
        return champion_stats.champion.champion_id

    def get_role(self, champion_stats):
        lane = champion_stats.bucket.lane
        role = champion_stats.bucket.role

        for combo in VALID_LANE_ROLE_COMBOS:
            if combo['lane'] == lane and combo['role'] == role:
                if 'alias' in combo.keys():
                    return combo['alias']
                else:
                    return '{} {}'.format(combo['lane'], combo['role'])

    class Meta:
        model = ChampionStats
        fields = ['avg_{}'.format(f) for f in Champion.aggregable_participant_fields] + \
                 ['name', 'champion_id', 'role', 'id']