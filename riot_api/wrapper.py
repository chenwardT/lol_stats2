"""
A wrapper for for the Celery task that uses the RiotWatcher instance.
"""

import logging
from datetime import datetime

import pytz

from lol_stats2.celery import (app,
                               riot_api,
                               store_get_summoner,
                               store_get_summoners,
                               store_static_get_champion_list,
                               store_static_get_summoner_spell_list,
                               store_get_recent_games,
                               store_get_challenger,
                               store_get_league,
                               store_get_match)
from matches.models import MatchDetail
from summoners.models import Summoner

logger = logging.getLogger(__name__)

# TODO: Lots of repetition of strings here.
# Consider putting all "store" methods in a class.
# Also, using a single string containing a method name to control flow.

class RiotAPI:
    # TODO: Consolidate with get_summoners.
    @staticmethod
    def get_summoner(name=None, region=None):
        """
        Gets and stores a single summoner given name and region.
        """
        func = 'get_summoner'
        kwargs = {'name': name, 'region': region}

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_summoner.s(region=region))

    @staticmethod
    def get_summoners(names=None, ids=None, region=None):
        """
        Gets and stores a list of summoners by name or ID for a given region.
        """
        func = 'get_summoners'
        kwargs = {'names': names, 'ids': ids, 'region': region}

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_summoners.s(region=region))

    @staticmethod
    def static_get_champion_list(region=None, locale=None, version=None,
                                 data_by_id=None, champ_data=None):
        """
        Gets and stores the list of champions.
        """
        func = 'static_get_champion_list'
        kwargs = {'region': region, 'locale': locale, 'version': version,
                  'data_by_id': data_by_id, 'champ_data': champ_data}

        return riot_api.apply_async((func, kwargs),
                                    link=store_static_get_champion_list.s())

    @staticmethod
    def static_get_summoner_spell_list(region=None, locale=None, version=None,
                                       data_by_id=None, spell_data=None):
        """
        Gets and stores the list of summoner spells.
        """
        func = 'static_get_summoner_spell_list'
        kwargs = {'region': region, 'locale': locale, 'version': version,
                  'data_by_id': data_by_id, 'spell_data': spell_data}

        return riot_api.apply_async((func, kwargs),
                                    link=store_static_get_summoner_spell_list.s())

    @staticmethod
    def get_recent_games(summoner_id, region=None):
        func = 'get_recent_games'
        kwargs = {'summoner_id': summoner_id, 'region': region}

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_recent_games.s(summoner_id=summoner_id,
                                                                  region=region))

    @staticmethod
    def get_challenger(region=None):
        """
        Gets and stores the challenger league for the given region.
        """
        func = 'get_challenger'
        kwargs = {'region': region}

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_challenger.s(region=region))

    @staticmethod
    def get_league(summoner_ids, region=None):
        """
        Gets and stores leagues for the given summoner IDs in the given
        region.

        Also updates any extant related summoners' last_leagues_update
        fields to now.
        """
        func = 'get_league'

        if isinstance(summoner_ids, int):
            kwargs = {'summoner_ids': [summoner_ids], 'region': region}

            summoner_query = Summoner.objects.filter(summoner_id=summoner_ids,
                                                     region=region)
            if summoner_query.exists():
                now = datetime.now(tz=pytz.utc)
                summoner = summoner_query.get()
                summoner.last_leagues_update = now
                summoner.save()
                logger.info('Set {} last_leagues_update to now: {}'
                            .format(summoner, now))
        else:
            kwargs = {'summoner_ids': summoner_ids, 'region': region}

            for id in summoner_ids:
                summoner_query = Summoner.objects.filter(summoner_id=id,
                                                         region=region)
                if summoner_query.exists():
                    now = datetime.now(tz=pytz.utc)
                    summoner = summoner_query.get()
                    summoner.last_leagues_update = now
                    summoner.save()
                    logger.info('Set {} last_leagues_update to now: {}'
                                .format(summoner, now))

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_league.s(summoner_ids, region))

    @staticmethod
    def get_match(match_id, region=None, include_timeline=False, check=True):
        """
        Gets a single match, timeline data optionally included.

        If `check` is True, the match won't be fetched if it is already stored.

        Note: Timeline data models not implemented.
        """
        func = 'get_match'
        kwargs = {'match_id': match_id,
                  'region': region,
                  'include_timeline': include_timeline}

        if check and not MatchDetail.objects.filter(match_id=match_id,
                                                    region=region.upper()).exists():
            return riot_api.apply_async((func, kwargs),
                                        link=store_get_match.s())
        else:
            return riot_api.apply_async((func, kwargs),
                                        link=store_get_match.s())

    # ENDPOINT REMOVED
    @staticmethod
    def get_match_history(summoner_id, region=None, champion_ids=None,
                          ranked_queues='RANKED_SOLO_5x5', begin_index=None,
                          end_index=None):
        """
        Gets a range of matches (max 15), based on indices.

        Used to get a list of match IDs to feed into get_match,
        via get_matches_from_ids.

        Also updates any extant related summoners' last_matches_update
        fields to now.
        """
        _ALLOWED_QUEUES = ('RANKED_SOLO_5x5', 'RANKED_TEAM_5x5')
        func = 'get_match_history'
        kwargs = {'summoner_id': summoner_id,
                  'region': region,
                  'champion_ids': champion_ids,
                  'ranked_queues': ranked_queues,
                  'begin_index': begin_index,
                  'end_index': end_index}

        if ranked_queues not in _ALLOWED_QUEUES:
            logger.error('Unsupported value for "ranked_queues": {};'
                         'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                         .format(ranked_queues))
            raise ValueError('Unsupported value for "ranked_queues": {};'
                             'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                             .format(ranked_queues))
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
                logger.info('Set {} last_matches_update to now: {}'
                            .format(summoner, now))

            return riot_api.apply_async((func, kwargs),
                                        link=get_matches_from_ids.s(region))

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
    @staticmethod
    def get_match_list(summoner_id, region=None, champion_ids=None, ranked_queues=None,
                       seasons=None, begin_time=None, end_time=None, begin_index=None,
                       end_index=None):
        """
        Gets all matches that satisfy the filters (args).

        Used to get a list of match IDs to feed into get_match,
        via get_matches_from_ids.

        Also updates any extant related summoners' last_matches_update
        fields to now.
        """
        _ALLOWED_QUEUES = ('RANKED_SOLO_5x5', 'RANKED_TEAM_5x5')
        func = 'get_match_list'
        kwargs = {'summoner_id': summoner_id,
                  'region': region,
                  'champion_ids': champion_ids,
                  'ranked_queues': ranked_queues,
                  'seasons': seasons,
                  'begin_time': begin_time,
                  'end_time': end_time,
                  'begin_index': begin_index,
                  'end_index': end_index}

        if ranked_queues not in _ALLOWED_QUEUES:
            # TODO: Factor out these msgs.
            logger.error('Unsupported value for "ranked_queues": {};'
                         'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                         .format(ranked_queues))
            raise ValueError('Unsupported value for "ranked_queues": {};'
                             'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                             .format(ranked_queues))
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
                logger.info('Set {} last_matches_update to now: {}'
                            .format(summoner, now))

            return riot_api.apply_async((func, kwargs),
                                        link=get_matches_from_ids.s(region))


@app.task(ignore_result=True)
def get_matches_from_ids(result, region):
    """
    Callback that parses the result dict for match IDs and feeds them back to
    the get_match for getting each match's full dataset (this method's received
    `result` only contains the data for the summoner ID that was passed to it).

    Returns a count of the matches that were saved (cached match data is not
    fetched).

    Note: Only works with matches of type 5x5, which are the only ones allowed
    by RiotAPI.get_match_history.
    """
    saved = 0

    if 'matches' in result:
        logger.debug('{} matches in result'.format(len(result['matches'])))

        result_ids = set([match['matchId'] for match in result['matches']])
        known_ids = set(MatchDetail.objects.filter(match_id__in=result_ids)
                        .values_list('match_id', flat=True))
        ids_to_query = result_ids - known_ids

        # Use check=False b/c we just checked that these match IDs
        # aren't known.
        for id in ids_to_query:
            RiotAPI.get_match(id, region, check=False)
            saved += 1

    logger.info('Got {} new matches'.format(saved))
