from rest_framework import viewsets

from .models import SummonerSpell
from .serializers import SummonerSpellSerializer

class SummonerSpellViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SummonerSpell.objects.all()
    serializer_class = SummonerSpellSerializer