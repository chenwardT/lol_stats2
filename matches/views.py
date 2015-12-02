import logging

from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from summoners.models import Summoner
from .models import MatchDetail
from .serializers import MatchDetailSerializer

logger = logging.getLogger(__name__)


class MatchDetailResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MatchDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchDetail.objects.all()
    serializer_class = MatchDetailSerializer
    pagination_class = MatchDetailResultsSetPagination


class MatchListForSummoner(generics.ListAPIView):
    """
    This view should return a list of all the matches for
    the summoner as determined by the summoner_pk portion
    of the URL.

    It returns matches in sets of at most 10.
    """
    serializer_class = MatchDetailSerializer
    pagination_class = MatchDetailResultsSetPagination

    def get_queryset(self):
        summoner_pk = self.kwargs['summoner_pk']
        return Summoner.objects.get(pk=summoner_pk).matches(10)
