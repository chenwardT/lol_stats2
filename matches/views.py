from rest_framework import viewsets

from .models import MatchDetail
from .serializers import MatchDetailSerializer

class MatchDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchDetail.objects.all()
    serializer_class = MatchDetailSerializer
