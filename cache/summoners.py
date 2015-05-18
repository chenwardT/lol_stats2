"""
Management classes for data that is relied upon by user-facing pages.

ex. Summary page for summoner A requires data on X, Y, and Z.
    Ensure X, Y, Z is fresh data, if not then update whatever is stale.
"""

import logging
import pytz
from datetime import datetime

from summoners.models import Summoner
from riot_api.wrapper import RiotAPI

logger = logging.getLogger(__name__)

class SingleSummoner:
    """
    Contains methods required to maintain the front-end's summoner page.
    """
    def __init__(self, region, std_name):
        self.std_name = std_name
        self.region = region
        self.summoner = None

    def is_known(self):
        query = Summoner.objects.filter(region=self.region,
                                        std_name=self.std_name)

        return query.exists()

    # TODO: Cache this.
    def get_handle(self):
        try:
            self.summoner = Summoner.objects.get(region=self.region,
                                                 std_name=self.std_name)
        except Exception as e:
            logger.exception(e)

        return self.summoner

    def if_known_get_handle(self):
        if self.is_known():
            return self.get_handle()
        else:
            return None

    def is_cache_fresh(self):
        """
        Returns True if this summoner's data is cached and the entry is fresh,
        otherwise False.
        """
        # TODO: Iterate over a list of models that we depend on, checking
        # each model instance's last_update and comparing it to it's cache life.
        return datetime.now(tz=pytz.utc) < (self.get_handle().last_update
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
        RiotAPI.get_summoner(region=self.region, name=self.std_name)

    def partial_query(self):
        """
        Performs a query of:
        -teams
        -league
        -match history
        -stats summary
        -ranked stats
        """
