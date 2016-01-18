"""
Ensures Summoner pages contain up-to-date data.
"""

import logging
from datetime import datetime, timedelta

import pytz
from django.db import transaction

from summoners.models import Summoner, InvalidSummonerQuery
from leagues.models import LeagueEntry
from riot_api.wrapper import RiotAPI
from utils.functions import coalesce_task_ids

logger = logging.getLogger(__name__)


class SingleSummoner:
    """
    Contains methods required to maintain the front end's summoner detail page.

    Expected to receive region and either A) summoner_id or B) name.
    The name is converted to the standardized name.
    A name is expected to be received when initialized by user actions
    (ex. a user searching for a summoner would be by region + name).

    After initialization, the expected use is determining if the summoner
    is known (stored in the DB).

    If it is known, the page can be loaded w/whatever data we have on them.

    If they are not known, then we have to perform a full query.

    Additionally, a partial query can be performed by the user which refreshes
    data using the region passed to __init__, but uses the summoner ID since
    that will always refer to the same account.
    """
    _ALLOWED_REGIONS = ('BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE',
                        'TR', 'RU')
    _SUMMONER_UPDATE_INTERVAL = timedelta(minutes=15)
    _MATCH_HISTORY_UPDATE_INTERVAL = timedelta(minutes=15)
    _LAST_MATCH_TIME_THRESHOLD = timedelta(minutes=15)
    _LEAGUE_UPDATE_INTERVAL = timedelta(minutes=15)

    # TODO: Rewrite init to not wait on get_summoners if we don't already know the summoner.
    def __init__(self, name=None, summoner_id=None, region=None):
        # These attributes are only used to get the summoner instance
        # and should not be referenced after __init__ completes.
        # TODO: change from object scope to method scope?
        self.std_name = name.lower().replace(' ', '') if name else None
        self.summoner_id = summoner_id
        self.region = region.upper()
        self.summoner = None

        logger.info('Summoner init started, name: {}, ID: {}, region: {}'.format(
            self.std_name, self.summoner_id, self.region))

        # TODO: Should this be caught at a lower level, and then we can
        # try/except here and include exc_info in log?
        if self.region not in self._ALLOWED_REGIONS:
            logger.error('Invalid region: {}; must be one of {}'
                         .format(self.region, self._ALLOWED_REGIONS))
            raise ValueError('Invalid region: {}; must be one of {}'
                             .format(self.region, self._ALLOWED_REGIONS))

        if not (self.summoner_id or self.std_name):
            logger.error('Expecting summoner_id or name to be present.')
            raise ValueError('Expecting summoner_id or name to be present.')

        # If the summoner isn't already known, the first time we get it
        # will be via name, meaning we have a std_name to work with.
        # if not self.is_known():
        #     logger.info('Summoner not known, querying Riot for: [{}] {}'
        #                 .format(self.region, self.std_name))
        #     task = RiotAPI.get_summoners(names=self.std_name, region=self.region)
        #
        #     # TODO: When invoked by ajax, must expose task ID to frontend
        #     # so data fetching progress can be seen/acted upon, also
        #     # remove synchronous behavior here.
        #
        #     # DEBUG - for console use
        #     # Wait until result is stored.
        #     while not task.successful():
        #         print('.', end='', flush=True)
        #         time.sleep(.5)

        # DEBUG - for console use
        # print('Retrieved {}'.format(self.get_instance()))
        # logger.info('Summoner init complete, {}'.format(self.get_instance()))

    def first_time_query(self):
        """
        Synchronous query of Riot API for summoner that isn't known.
        All tasks must finish before summoner detail page load.

        If 404 response, then show "Summoner not found" page.
        Else follow up with a full query of everything else and load summoner detail page.

        Returns True if the summoner exists (and was fetched or updated), else False.
        """
        query_start = datetime.now()
        result = self._query_summoner_by_name().get()

        if result['created'] == 0 and result['updated'] == 0:
            blacklisted = InvalidSummonerQuery(name=self.std_name, region=self.region)
            blacklisted.save()
            logger.debug('Blacklisting query for %s: %s',
                         InvalidSummonerQuery.TTL, blacklisted)

        # TODO: result['updated'] should never equal 1 since this is a first-time query?
        # Investigate potential for race condition.
        if result['created'] == 1 or result['updated'] == 1:
            self.get_instance().set_last_full_update()
            self.blocking_full_query()

            logger.info('complete: found summoner and got data ({})'.format(datetime.now() - query_start))
            return True
        else:
            logger.info('complete: did not find summoner ({})'.format(datetime.now() - query_start))
            return False

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

    def is_invalid_query(self):
        return InvalidSummonerQuery.objects.contains(name=self.std_name, region=self.region)

    def _query_summoner_by_name(self):
        return RiotAPI.get_summoners(names=self.std_name, region=self.region)

    def _query_summoner_by_id(self):
        return RiotAPI.get_summoners(ids=self.summoner_id, region=self.region)

    def get_instance(self):
        """
        Get the appropriate model instance and cache it to self.summoner.

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

    def _query_match_history(self):
        return RiotAPI.get_match_list(summoner_id=self.summoner.summoner_id,
                                      region=self.summoner.region)

    def _query_league(self):
        return RiotAPI.get_league(summoner_ids=self.summoner.summoner_id, region=self.summoner.region)

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

    def _is_matches_fresh(self):
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

    def _is_leagues_fresh(self):
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

    def is_refreshable(self):
        """
        Returns True if enough time has passed since the summoner was last refreshed by a user
        to do it again, or if the summoner isn't known.

        Otherwise return False.
        """
        if self.is_known():
            return self.get_instance().is_refreshable()
        else:
            # This may be a good place to address unlimited querying of invalid summoners.
            # See https://github.com/chenwardT/lol_stats2/issues/24
            return True

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
        logger.info('started on [{}] {}'.format(self.region, self.std_name))
        self.get_instance().set_last_full_update()
        match_job = self._query_match_history()
        league_job = self._query_league()

        # This gets returned to the frontend. The frontend shows "Loading" until it gets a
        # positive response from multi_task_status. Then it can load the new data!
        return coalesce_task_ids([match_job, league_job])

    def blocking_full_query(self):
        logger.info('started on [{}] {}'.format(self.region, self.std_name))

        self._query_match_history().get()
        self._query_league().get()

        logger.info('complete')

    def partial_query(self):
        """
        Performs a query of:
        -teams
        -league
        -match history
        -stats summary
        -ranked stats
        """
        pass

    def query_if_no_league(self):
        with transaction.atomic():
            if not LeagueEntry.objects.filter(player_or_team_id=self.summoner.summoner_id,
                                              league__region=self.summoner.region).exists():
                self._query_league()
