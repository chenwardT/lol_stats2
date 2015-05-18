from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from summoners.views import SummonerViewSet, index, search, show, refresh
from champions.views import ChampionViewSet

router = routers.DefaultRouter()
router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lol_stats2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^home/', index),
    url(r'^show/(?P<name>\w+)', show, name='show'),
    url(r'^search/', search),
    url(r'^refresh/', refresh, name='refresh'),

    url(r'^admin/', include(admin.site.urls)),
)
