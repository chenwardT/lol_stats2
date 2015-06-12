"""
Management class for summoner data retrieval.
"""

import logging
import pytz
from datetime import datetime

from summoners.models import Summoner
from riot_api.wrapper import RiotAPI

logger = logging.getLogger(__name__)

# TODO: Consider a usage pattern where we can call get_handle in __init__() or
# something instead of in each method that needs a handle.
class SingleSummoner:
    """
    Contains methods required to maintain the front-end's summoner page.
    """
    def __init__(self, region, std_name):
        self.std_name = std_name
        self.region = region
        self.summoner = None

    def is_known(self):
        return Summoner.objects.is_known(name=self.std_name,
                                         region=self.region)

    def get_instance(self):
        if self.summoner is None:
            try:
                self.summoner = Summoner.objects.get(region=self.region,
                                                     std_name=self.std_name)
            except Exception as e:
                logger.exception(e)

        return self.summoner

    def if_known_get_handle(self):
        if self.is_known():
            return self.get_instance()
        else:
            return None

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
        self.get_summoner()

    def partial_query(self):
        """
        Performs a query of:
        -teams
        -league
        -match history
        -stats summary
        -ranked stats
        """

    def get_summoner(self):
        RiotAPI.get_summoner(region=self.region, name=self.std_name)

    def get_recent_games(self):
        logger.info('Summoner - Recent Games Query on [{}] {}'.format(self.region, self.std_name))

        # If this is a new summoner.
        if not self.is_known():
            self.get_summoner()

        self.get_instance()

        RiotAPI.get_recent_games(summoner_id=self.summoner.summoner_id,
                                 region=self.region)