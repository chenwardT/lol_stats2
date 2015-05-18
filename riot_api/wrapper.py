"""
A wrapper for for the Celery task that uses the RiotWatcher instance.
"""

from lol_stats2.celery import riot_api, store_get_summoner

class RiotAPI:
    @staticmethod
    def get_summoner(name=None, region=None):
        func = 'get_summoner'
        kwargs = {'name': name, 'region': region}

        job = riot_api.apply_async((func, kwargs),
                                   link=store_get_summoner.s(region=region))
