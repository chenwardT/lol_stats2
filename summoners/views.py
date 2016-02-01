import logging
import json

from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Summoner
from .serializers import SummonerSerializer
from .forms import SearchForm
from cache.summoners import SingleSummoner
from utils.functions import standardize_name
from utils.constants import REGIONS

logger = logging.getLogger(__name__)

SUMMONER_NOT_FOUND_PK = -1


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
    print(request.body)
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect('show', name=form.cleaned_data['name'], region=form.cleaned_data['region'])
    else:
        form = SearchForm()
        return render(request, 'summoners/search.html', {'form': form})

def query_is_valid(query):
    if 'name' in query and 'region' in query:
        region = query['region']

        if region in REGIONS:
            return True

    return False

@csrf_exempt
def get_pk_from_region_and_summoner(request):
    """
    Returns a Summoner PK given a region and summoner name.
    """
    query = json.loads(request.body.decode('utf-8'))
    print(repr(query))

    if query_is_valid(query):
        summoner = Summoner.objects.filter(region=query['region'],
                                           std_name=standardize_name(query['name']))

        if summoner.exists():
            data = summoner.values('id', 'region', 'name')[0]
        else:
            data = SUMMONER_NOT_FOUND_PK

        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')

@ensure_csrf_cookie
def show(request, name, region):
    ss = SingleSummoner(name=name, region=region)

    if ss.is_invalid_query():
        logger.info('Temporarily blacklisted query detected: [%s] %s', ss.region, ss.std_name)
        return render(request, 'summoners/not_found.html')

    if ss.is_known():
        ss.get_instance()
        return render(request, 'summoners/show.html',
                      {'summoner': ss.summoner,
                       'name': ss.summoner.name,
                       'recent_matches': ss.summoner.matches(10)})
    else:
        if ss.first_time_query():
            return render(request, 'summoners/show.html',
                          {'summoner': ss.summoner,
                           'name': ss.summoner.name,
                           'recent_matches': ss.summoner.matches(10)})
        else:
            return render(request, 'summoners/not_found.html')


def refresh(request):
    if request.method == 'POST':
        logger.debug(request.POST)
        name = request.POST['name']

        ss = SingleSummoner(name=name, region='NA')
        ss.get_instance()
        task_ids = ss.full_query()

        return JsonResponse({'task_ids': task_ids})


def is_summoner_refreshable(request):
    if request.method == 'POST':
        logger.debug(request.POST)
        name = request.POST['name']
        region = request.POST['region']
        ss = SingleSummoner(name=name, region=region)

        return JsonResponse({'refreshable': ss.is_refreshable()})
    else:
        return HttpResponseBadRequest
