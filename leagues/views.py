from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from summoners.models import Summoner
from .models import League
from .serializers import LeagueSerializer


class LeagueResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    pagination_class = LeagueResultsSetPagination


class LeagueEntryForSummoner(generics.RetrieveAPIView):
    """
    This view should return the 5v5 solo queue league for
    the summoner as determined by the summoner_pk portion
    of the URL.
    """
    serializer_class = LeagueSerializer
    pagination_class = LeagueResultsSetPagination

    def get_queryset(self):
        summoner_pk = self.kwargs['summoner_pk']
        return Summoner.objects.get(pk=summoner_pk).league_entry()
