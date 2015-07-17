from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import MatchDetail
from .serializers import MatchDetailSerializer

class MatchDetailResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MatchDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchDetail.objects.all()
    serializer_class = MatchDetailSerializer
    pagination_class = MatchDetailResultsSetPagination