from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

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
