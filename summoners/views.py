from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Summoner
from .serializers import SummonerSerializer
from .forms import SearchForm
from cache.summoners import SingleSummoner

class SummonerResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SummonerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer
    pagination_class = SummonerResultsSetPagination


def index(request):
    recent_summoners = Summoner.objects.all().order_by('-last_update')[:5]
    return render(request, 'summoners/index.html',
                  {'recent_summoners': recent_summoners})

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect('show', name=form.cleaned_data['name'])
    else:
        form = SearchForm()

    return render(request, 'summoners/search.html', {'form': form})

def show(request, name):
    q = Summoner.objects.filter(name=name, region='na')

    if q.exists():
        summoner = q[0]
    else:
        summoner = None

    return render(request, 'summoners/show.html',
                  {'summoner': summoner, 'name': name})

def refresh(request):
    if request.method == 'POST':
        name = request.POST['name']

        ss = SingleSummoner(region='na', std_name=name)
        ss.full_query()

    return redirect('show', name=name)
