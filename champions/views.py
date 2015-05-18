from rest_framework import viewsets

from .models import Champion
from .serializers import ChampionSerializer

class ChampionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer
