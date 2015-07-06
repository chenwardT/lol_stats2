"""
Ensures Summoner pages contain up-to-date data.
"""

import logging
from datetime import datetime
import time

import pytz

from summoners.models import Summoner
from riot_api.wrapper import RiotAPI
from lol_stats2.celery import app, riot_api, store_get_summoner

logger = logging.getLogger(__name__)

class SingleSummoner:
    """
    Contains methods required to maintain the front-end's summoner page.

    Expected to receive region and either A) summoner_id or B) std_name.
    A name is expected to be received when initialized by user actions
    (ex. a user searching for a summoner would be by region + name).
    """
    _ALLOWED_REGIONS = ('BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE',
                        'TR', 'RU')

    def __init__(self, std_name=None, summoner_id=None, region=None):
        # These attributes are only used to get the summoner instance
        # and should not be referenced after __init__ completes.
        self.std_name = std_name
        self.summoner_id = summoner_id
        self.region = region
        self.summoner = None

        if self.region not in self._ALLOWED_REGIONS:
            raise ValueError('Invalid region: {}; must be one of {}'
                             .format(self.region, self._ALLOWED_REGIONS))

        if not (self.summoner_id or self.std_name):
            raise ValueError('Expecting summoner_id or std_name to be present.')

        # If the summoner isn't already known, the first time we get it
        # will be via name, meaning we have a std_name to work with.
        if not self.is_known():
            task = riot_api.apply_async(('get_summoner',
                                         {'name': self.std_name,
                                          'region': self.region}),
                                        link=store_get_summoner.s(region=region))

            # Wait until result is stored.

            while task.children is None:
                print('.', end='',flush=True)
                time.sleep(.1)

            while task.children[0].status != 'SUCCESS':
                print('_', end='',flush=True)
                time.sleep(.1)

        print('Retrieved {}'.format(self.get_instance()))

    def is_known(self):
        if self.summoner_id:
            return Summoner.objects.filter(summoner_id=self.summoner,
                                           region=self.region).exists()
        else:
            return Summoner.objects.filter(std_name=self.std_name,
                                           region=self.region).exists()

    def get_summoner_by_name(self):
        RiotAPI.get_summoner(region=self.region, name=self.std_name)

    def get_summoner_by_id(self):
        RiotAPI.get_summoners(region=self.region, ids=[self.summoner.summoner_id])

    def get_instance(self):
        """
        Get the appropriate model instance and assign it to self.summoner.

        Returns summoner instance if found, otherwise None.
        """
        if self.summoner is None:
            if self.summoner_id:
                summoner_query = Summoner.objects.filter(region=self.region,
                                                         summoner_id=self.summoner_id)

                if summoner_query.exists():
                    self.summoner = summoner_query.get()
            else:
                summoner_query = Summoner.objects.filter(region=self.region,
                                                         std_name=self.std_name)

                if summoner_query.exists():
                    self.summoner = summoner_query.get()

        return self.summoner

    def get_match_history(self):
        RiotAPI.get_match_history(summoner_id=self.summoner.summoner_id,
                                  region=self.summoner.region)

    def get_league(self):
        RiotAPI.get_league(self.summoner.summoner_id, self.summoner.region)

    def is_cache_fresh(self):
        """
        Returns True if this summoner's data is cached and the entry is fresh,
        otherwise False.
        """
        # TODO: Iterate over a list of models that we depend on, checking
        # each model instance's last_update and comparing it to it's cache life.
        # Alternatively, check caches for each model instead of everything we depend
        # on to further more granular cache refreshing.
        return datetime.now(tz=pytz.utc) < (self.get_instance().last_update
                                            + Summoner.CACHE_DURATION)

    def full_query(self):
        """
        Performs a query of all endpoints required to populate page:
        -summoner, by name
        -teams
        -league
        -match history
        -stats summary of this season
        -stats summary of last season
        -ranked stats of this season
        -ranked stats of last season
        """
        logger.info('Summoner - Full Query on [{}] {}'.format(self.region, self.std_name))

        # TODO: This should probably just be a list of calls to methods on this class.
        self.get_summoner_by_id()
        self.get_match_history()
        self.get_league()

    def partial_query(self):
        """
        Performs a query of:
        -teams
        -league
        -match history
        -stats summary
        -ranked stats
        """

    # def get_recent_games(self):
    #     logger.info('Summoner - Recent Games Query on [{}] {}'.format(self.region, self.std_name))
    #
    #     # If this is a new summoner.
    #     if not self.is_known():
    #         self.get_summoner_by_name()
    #
    #     self.get_instance()
    #
    #     RiotAPI.get_recent_games(summoner_id=self.summoner.summoner_id,
    #                              region=self.region)

@app.task
def get_summoner_task(std_name, region):
    riot_api.apply_async(('get_summoner', {'name': std_name,'region': region}),
                         link=store_get_summoner.s(region=region))