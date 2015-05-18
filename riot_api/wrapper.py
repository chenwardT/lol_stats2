"""
A wrapper for for the Celery task that uses the RiotWatcher instance.
"""

from lol_stats2.celery import (riot_api,
                               store_get_summoner,
                               store_static_get_champion_list)

# TODO: Lots of repetition of strings here.
# Consider putting all "store" methods in a class.
# Also, using a single string containing a method name to control flow.

class RiotAPI:
    @staticmethod
    def get_summoner(name=None, region=None):
        func = 'get_summoner'
        kwargs = {'name': name, 'region': region}

        job = riot_api.apply_async((func, kwargs),
                                   link=store_get_summoner.s(region=region))

    @staticmethod
    def static_get_champion_list(region=None, locale=None, version=None,
                                 data_by_id=None, champ_data=None):
        func = 'static_get_champion_list'
        kwargs = {'region': region, 'locale': locale, 'version': version,
                  'data_by_id': data_by_id, 'champ_data': champ_data}

        job = riot_api.apply_async((func, kwargs),
                                   link=store_static_get_champion_list.s())