import logging
import pytz
from datetime import timedelta, datetime

from summoners.models import Summoner
from riot_api.wrapper import RiotAPI

logger = logging.getLogger(__name__)

class SingleSummoner:
    """
    Contains methods required to maintain the front-end's summoner page.
    """
    # TODO: Set to something reasonable; 20 min?
    CACHE_EXPIRE = timedelta(minutes=1)

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

    def is_cache_fresh(self):
        """
        Returns True if this summoner's data is cached and the entry is fresh,
        otherwise False.
        """
        return datetime.now(tz=pytz.utc) < (self.get_handle().last_update
                                            + self.CACHE_EXPIRE)

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

    def store_data(self):
        """
        Stores data in Postgres.
        """