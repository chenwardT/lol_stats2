"""
A wrapper for for the Celery task that uses the RiotWatcher instance.
"""

import logging
from datetime import datetime, timedelta

import pytz
from celery import chain, group

from lol_stats2.celery import (app,
                               riot_api,
                               store_match,
                               store_summoners,
                               store_league,
                               store_summoner_spell_list)
from matches.models import MatchDetail
from summoners.models import Summoner

logger = logging.getLogger(__name__)


class RiotAPI:
    """
    This class contains static methods to generate arguments to pass to riot_api
    as well as tasks related to chained operations, like getting a summoner's matches.
    """
    @staticmethod
    def get_summoners(names=None, ids=None, region=None):
        """
        Gets and stores a list of summoners by name or ID for a given region.
        """
        # Coerce to list if a single name or id
        if isinstance(names, str):
            names = list((names,))

        if isinstance(ids, int):
            ids = list((ids,))

        kwargs = {'method': 'get_summoners', 'names': names, 'ids': ids, 'region': region.lower()}

        return chain(riot_api.s(kwargs), store_summoners.s(region=region))()

    @staticmethod
    def static_get_champion_list(region=None, locale=None, version=None,
                                 data_by_id=None, champ_data=None):
        """
        Gets and stores the list of champions.
        """
        kwargs = {'method': 'static_get_champion_list',
                  'region': region,
                  'locale': locale,
                  'version': version,
                  'data_by_id': data_by_id,
                  'champ_data': champ_data}

        return kwargs

    @staticmethod
    def static_get_summoner_spell_list(region=None, locale=None, version=None,
                                       data_by_id=None, spell_data=None):
        """
        Gets and stores the list of summoner spells.
        """
        kwargs = {'method': 'static_get_summoner_spell_list',
                  'region': region,
                  'locale': locale,
                  'version': version,
                  'data_by_id': data_by_id,
                  'spell_data': spell_data}

        return chain(riot_api.s(kwargs), store_summoner_spell_list.s())()

    # Unused, see Game vs MatchDetail (this is unranked matches)
    @staticmethod
    def get_recent_games(summoner_id, region=None):
        kwargs = {'method': 'get_recent_games',
                  'summoner_id': summoner_id,
                  'region': region}

        return kwargs

    @staticmethod
    def get_challenger(region=None):
        """
        Gets and stores the challenger league for the given region.
        """
        kwargs = {'method': 'get_challenger',
                  'region': region}

        return kwargs

    # TODO: Set a reasonable default ttl.
    @staticmethod
    def get_league(summoner_ids, region=None, ttl=timedelta(seconds=1)):
        """
        Gets and stores leagues for the given summoner IDs in the given
        region.

        Also updates any extant related summoners' last_leagues_update
        fields to now.
        """
        ignorable = set()

        # Coerce to set if only a single summoner ID.
        if isinstance(summoner_ids, int):
            summoner_ids = {summoner_ids}
        else:
            summoner_ids = set(summoner_ids)

        for summoner_id in summoner_ids:
            summoner_query = Summoner.objects.filter(summoner_id=summoner_id, region=region.upper())

            # Since we can only query leagues through summoners,
            # and we don't know who is in the league yet,
            # we track league update times on summoners,
            # and thus can only update them if the summoner is known.
            if summoner_query.exists():
                now = datetime.now(tz=pytz.utc)
                summoner = summoner_query.get()

                # Allow the update to proceed if ttl has expired.
                if summoner.last_leagues_update is None or \
                   datetime.now(tz=pytz.utc) - summoner.last_leagues_update > ttl:
                    summoner.last_leagues_update = now
                    summoner.save()
                    logger.info('Set {} last_leagues_update to now: {}'.format(summoner, now))
                else:
                    ignorable.add(summoner_id)

        to_query = summoner_ids - ignorable
        logger.debug('to_query: {}'.format(to_query))

        kwargs = {'method': 'get_league',
                  'summoner_ids': list(to_query),
                  'region': region.lower()}

        if len(to_query) != 0:
            return chain(riot_api.s(kwargs), store_league.s(region=region))()
        else:
            logger.warning('No valid summoners to get leagues of.')

    # TODO: There is no upper limit on the number of match IDs that can be
    # retrieved now, so we need to consider how to handle large amounts of
    # "new" matches being found. This can occur if a summoner doesn't get
    # refreshed for a long time (during which they participate in many matches).
    #
    # This issue can also be (better?) handled in get_matches_from_ids,
    # where we can just get, e.g. the 10 most recent matches that are not already
    # in the DB.
    #
    # Something more complex may be required for intuitive behavior to the user.
    # For example, if more than 10 matches were played *since last time we fetched*,
    # then just get the most recent 10.
    #
    # This stands in contrast to us getting 5 matches from before the presently known
    # matches and that occurred since the last fetch (what are the odds of this case?)
    # TODO: Consider removal of all ranked_queues options besides solo queue.
    @staticmethod
    def get_match_list(summoner_id, region=None, champion_ids=None, ranked_queues='RANKED_SOLO_5x5',
                       season=None, begin_time=None, end_time=None, begin_index=None,
                       end_index=None, max_matches=7):
        """
        Gets all matches that satisfy the filters (args) for the specified summoner ID.

        Reads match IDs from the response and starts a group of tasks that each get those
        matches.

        Also updates any extant related summoners' last_matches_update
        fields to now.

        Returns the executed group.
        """
        logger.info('Getting matches for {} [{}]'.format(summoner_id, region))

        _ALLOWED_QUEUES = ('RANKED_SOLO_5x5', 'RANKED_TEAM_5x5')

        kwargs = {'method': 'get_match_list',
                  'summoner_id': summoner_id,
                  'region': region,
                  'champion_ids': champion_ids,
                  'ranked_queues': ranked_queues,
                  'season': season,
                  'begin_time': begin_time,
                  'end_time': end_time,
                  'begin_index': begin_index,
                  'end_index': end_index}

        if ranked_queues not in _ALLOWED_QUEUES:
            error_msg = ('Unsupported value for "ranked_queues": {}; '
                         'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                         .format(ranked_queues))
            logger.error(error_msg)
            raise ValueError(error_msg)
        else:
            summoner_query = Summoner.objects.filter(region=region,
                                                     summoner_id=summoner_id)

            # TODO: This may be misleading, as the time of the actual
            # get_matches_from_ids or get_match calls don't necessarily
            # occur immediately after this executes, e.g. when queues
            # are backed up.
            # Possible solution: pass summoner ID through to
            # get_matches_from_ids and update last_matches_update field there.
            if summoner_query.exists():
                now = datetime.now(tz=pytz.utc)
                summoner = summoner_query.get()
                summoner.last_matches_update = now
                summoner.save()
                logger.info('Set {} last_matches_update to now: {}'.format(summoner, now))

            get_ids_chain = chain(riot_api.s(kwargs),
                                  RiotAPI.get_matches_from_ids.s(region=region,
                                                                 max_matches=max_matches))

            return group(chain(RiotAPI.get_match.s(match_id=match_id, region=region),
                               riot_api.s(),
                               store_match.s()) for match_id in get_ids_chain().get())()

    @app.task
    def get_match(match_id, region=None, include_timeline=False, execute=False):
        """
        Gets a single match, timeline data optionally included.

        If `check` is True, the match won't be fetched if it is already stored.
        This receives a list of match IDs from get_matches_from_ids.

        Note: Timeline data models not implemented.
        """
        kwargs = {'method': 'get_match',
                  'match_id': match_id,
                  'region': region,
                  'include_timeline': include_timeline}

        if not execute:
            return kwargs
        else:
            return chain(riot_api.s(kwargs), store_match.s())()

    # TODO: The region could be passed along with the match IDs so the caller of
    # the chain doesn't have to.
    @app.task
    def get_matches_from_ids(result, region, max_matches=10, recent_first=True):
        """
        Parses the result dict for match IDs, compares them to stored matches,
        and returns a list of match IDs that do not have corresponding matches
        stored in the database. Used as a callback in get_match_list after
        receiving a list of matches from Riot.

        max_matches specifies the maximum number of matches to fetch from the result
        dict.

        If recent_first is set, the max_matches slice will be take the most recent
        matches (end of the dict), otherwise it will take the earliest.

        Note: Only works with matches of type 5x5, which are the only ones allowed
        by RiotAPI.get_match_list.
        """
        if 'matches' in result:
            logger.debug('{} matches in result'.format(len(result['matches'])))

            # Get max_matches from the beginning or end.
            if max_matches:
                if recent_first:
                    result['matches'] = result['matches'][:max_matches]
                else:
                    result['matches'] = result['matches'][-max_matches:]

            # Skip the matches that are already stored in the DB.
            result_ids = set([match['matchId'] for match in result['matches']])
            known_ids = set(MatchDetail.objects.filter(match_id__in=result_ids)
                            .values_list('match_id', flat=True))
            ids_to_query = list(result_ids - known_ids)

            logger.info('{} matches will be fetched.'.format(len(ids_to_query)))
        else:
            ids_to_query = []

        return ids_to_query
