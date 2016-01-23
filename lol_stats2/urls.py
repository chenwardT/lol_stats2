from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from summoners.views import SummonerViewSet, index, search, show, refresh
from champions.views import ChampionViewSet
from matches.views import MatchDetailViewSet, MatchListForSummoner
from leagues.views import LeagueViewSet, LeagueEntryForSummoner
from cache.views import task_status, is_summoner_refreshable
from stats.views import ChampionStatsByVersion

router = routers.DefaultRouter()
router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)
router.register(r'matchdetails', MatchDetailViewSet)
router.register(r'leagues', LeagueViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^summoner-matches/(?P<summoner_pk>\d+)', MatchListForSummoner.as_view()),
    url(r'^summoner-league/(?P<summoner_pk>\d+)', LeagueEntryForSummoner.as_view()),
    url(r'^champion-stats/(?P<patch>[\w.]+)', ChampionStatsByVersion.as_view()),

    url(r'^home/', index),
    url(r'^show/(?P<region>\w+)/(?P<name>[\w ]+)', show, name='show'),
    url(r'^search/', search, name='search'),
    url(r'^refresh/', refresh, name='refresh'),
    url(r'^task-status/', task_status, name='task_status'),
    url(r'^summoner-refreshable', is_summoner_refreshable, name='summoner_refreshable'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
