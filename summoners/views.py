from django.shortcuts import render
from rest_framework import viewsets

from .models import Summoner
from .serializers import SummonerSerializer


class SummonerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer