from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from summoners.views import SummonerViewSet, index, search, show, refresh
from champions.views import ChampionViewSet
from matches.views import MatchDetailViewSet
from leagues.views import LeagueViewSet
from cache.views import task_status

router = routers.DefaultRouter()
router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)
router.register(r'matchdetails', MatchDetailViewSet)
router.register(r'leagues', LeagueViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^home/', index),
    url(r'^show/(?P<name>\w+)', show, name='show'),
    url(r'^search/', search),
    url(r'^refresh/', refresh, name='refresh'),
    url(r'^task_status/', task_status, name='task_status'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
