from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Champion
from .serializers import ChampionSerializer

class ChampionResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ChampionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer
    # pagination_class = ChampionResultsSetPagination