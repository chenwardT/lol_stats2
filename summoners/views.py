from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
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
    recent_summoners = Summoner.objects.all().order_by('-last_update')[:20]
    return render(request, 'summoners/index.html',
                  {'recent_summoners': recent_summoners})


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect('show', name=form.cleaned_data['name'], region=form.cleaned_data['region'])
    else:
        form = SearchForm()

    return render(request, 'summoners/search.html', {'form': form})


@ensure_csrf_cookie
def show(request, name, region):
    ss = SingleSummoner(name=name, region=region)

    if ss.is_known():
        ss._get_instance()
        return render(request, 'summoners/show.html',
                      {'summoner': ss.summoner,
                       'name': ss.summoner.name,
                       'recent_matches': ss.summoner.matches()[:20]})
    else:
        if ss.first_time_query():
            return render(request, 'summoners/show.html',
                      {'summoner': ss.summoner,
                       'name': ss.summoner.name,
                       'recent_matches': ss.summoner.matches()[:20]})
        else:
            return render(request, 'summoners/show.html')


def refresh(request):
    if request.method == 'POST':
        name = request.POST['name']

        ss = SingleSummoner(name=name, region='NA')
        ss._get_instance()
        task_ids = ss.full_query()

        return JsonResponse({'task_ids': task_ids})
