"""
Ensures Summoner pages contain up-to-date data.
"""

import logging
from datetime import datetime, timedelta
import time

import pytz
from django.db import transaction

from summoners.models import Summoner
from leagues.models import LeagueEntry
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
    _SUMMONER_UPDATE_INTERVAL = timedelta(minutes=15)
    _MATCH_HISTORY_UPDATE_INTERVAL = timedelta(minutes=15)
    _LAST_MATCH_TIME_THRESHOLD = timedelta(minutes=15)
    _LEAGUE_UPDATE_INTERVAL = timedelta(minutes=15)

    # TODO: Can we combine error logging and exception raising?
    def __init__(self, std_name=None, summoner_id=None, region=None):
        # These attributes are only used to get the summoner instance
        # and should not be referenced after __init__ completes.
        self.std_name = std_name.lower()
        self.summoner_id = summoner_id
        self.region = region
        self.summoner = None

        logger.debug('Summoner init started, name: {}, ID: {}, region: {}'.format(
            self.std_name, self.summoner_id, self.region))

        # TODO: Should this be caught at a lower level, and then we can
        # try/except here and include exc_info in log?
        if self.region not in self._ALLOWED_REGIONS:
            logger.error('Invalid region: {}; must be one of {}'
                             .format(self.region, self._ALLOWED_REGIONS))
            raise ValueError('Invalid region: {}; must be one of {}'
                             .format(self.region, self._ALLOWED_REGIONS))

        if not (self.summoner_id or self.std_name):
            logger.error('Expecting summoner_id or std_name to be present.')
            raise ValueError('Expecting summoner_id or std_name to be present.')

        # If the summoner isn't already known, the first time we get it
        # will be via name, meaning we have a std_name to work with.
        if not self.is_known():
            task = RiotAPI.get_summoner(self.std_name, self.region)

            # TODO: When invoked by ajax, must expose task ID to frontend
            # so data fetching progress can be seen/acted upon, also
            # remove synchronous behavior here.

            # Wait until result is stored.

            while task.children is None:
                print('.', end='',flush=True)
                time.sleep(.1)

            while task.children[0].status != 'SUCCESS':
                print('_', end='',flush=True)
                time.sleep(.1)

        print('Retrieved {}'.format(self.get_instance()))
        logger.debug('Summoner init complete, {}'.format(self.get_instance()))

    def is_known(self):
        """
        Checks for the existence of the summoner in the database.

        Checks by summoner ID if a summoner ID was passed to __init__, otherwise
        uses the standardized name.
        """
        if self.summoner_id:
            return Summoner.objects.filter(summoner_id=self.summoner_id,
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
        Get the appropriate model instance and assign it to self.summoner, where
        it is cached.

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

    # # TODO: Consider calling self.summoner.refresh_from_db().
    # def is_cache_fresh(self):
    #     """
    #     Returns True if this summoner's data is in the DB and the entry is fresh,
    #     otherwise False.
    #     """
    #     # TODO: Iterate over a list of models that we depend on, checking
    #     # each model instance's last_update and comparing it to its cache life.
    #     # Alternatively, check caches for each model instead of everything we depend
    #     # on to further more granular cache refreshing.
    #     #
    #     # return datetime.now(tz=pytz.utc) < (self.get_instance().last_update
    #     #                                     + Summoner.CACHE_DURATION)

    def is_matches_fresh(self):
        """
        Returns True if either is true:

        1) This summoner's most recent match's creation datetime is within a time
           distance specified by _LAST_MATCH_TIME_THRESHOLD of now.

        2) The summoner's last_matches_update is within a time distance specified
           by _MATCH_HISTORY_UPDATE_INTERVAL of now.

        Otherwise returns False.

        If any of the checked fields are missing (None), then their respective
        clauses are considered False.
        """
        if self.summoner.most_recent_match_date() and self.summoner.last_matches_update:
            time_since_match = datetime.now(tz=pytz.utc) - self.summoner.most_recent_match_date()
            time_since_update = datetime.now(tz=pytz.utc) - self.summoner.last_matches_update

            return time_since_match < self._LAST_MATCH_TIME_THRESHOLD or \
                   time_since_update < self._MATCH_HISTORY_UPDATE_INTERVAL
        elif self.summoner.most_recent_match_date():
            time_since_match = datetime.now(tz=pytz.utc) - self.summoner.most_recent_match_date()

            return time_since_match < self._LAST_MATCH_TIME_THRESHOLD
        elif self.summoner.last_matches_update:
            time_since_update = datetime.now(tz=pytz.utc) - self.summoner.last_matches_update

            return time_since_update < self._MATCH_HISTORY_UPDATE_INTERVAL
        else:
            return False

    def is_leagues_fresh(self):
        """
        Returns True if the summoner's last_leagues_update is within a time
        distance of _LEAGUE_UPDATE_INTERVAL from now, otherwise False.

        If the summoner's last_leagues_update field is None, then returns False.
        """
        if self.summoner.last_leagues_update:
            time_since_leagues = datetime.now(tz=pytz.utc) - self.summoner.last_leagues_update

            return time_since_leagues < self._LEAGUE_UPDATE_INTERVAL
        else:
            return False

    def full_query(self):
        """
        Performs a query of all endpoints required to populate page:
        -summoner, by name or ID?
        -teams
        -league
        -match history
        -stats summary of this season
        -stats summary of last season
        -ranked stats of this season
        -ranked stats of last season
        """
        logger.debug('Summoner full query started on [{}] {}'.format(self.region, self.std_name))

        self.get_summoner_by_id()
        self.get_match_history()
        self.get_league()

        logger.debug('Summoner full query completed on [{}] {}'.format(self.region, self.std_name))

    def partial_query(self):
        """
        Performs a query of:
        -teams
        -league
        -match history
        -stats summary
        -ranked stats
        """

    def query_if_no_league(self):
        with transaction.atomic():
            if not LeagueEntry.objects.filter(player_or_team_id=self.summoner.summoner_id,
                                              league__region=self.summoner.region).exists():
                self.get_league()

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
