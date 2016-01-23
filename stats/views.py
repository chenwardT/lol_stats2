from django.db.models import Q
from rest_framework import generics

from champions.models import SignificantPosition
from .models import ChampionStats
from .serializers import ChampionStatsSerializer

class ChampionStatsByVersion(generics.ListAPIView):
    """
    Displays some stats for champions.
    """
    serializer_class = ChampionStatsSerializer

    def get_queryset(self):
        """
        Filter stats by match version.
        """
        version = self.kwargs['patch']
        queryset = ChampionStats.objects.select_related('bucket')\
                                        .select_related('champion')\
                                        .filter(bucket__version=version,
                                                bucket__region='ALL')

        q_objs = Q()
        for sp in SignificantPosition.objects.filter(version=version):
            q_objs |= Q(bucket__region='ALL', bucket__role=sp.role,
                        bucket__lane=sp.lane, champion_id=sp.champion_id)

        return queryset.filter(q_objs)