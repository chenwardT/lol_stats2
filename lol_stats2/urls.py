from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from summoners.views import SummonerViewSet

router = routers.DefaultRouter()
router.register(r'summoners', SummonerViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lol_stats2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
)
