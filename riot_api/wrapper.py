"""
A wrapper for for the Celery task that uses the RiotWatcher instance.
"""

from lol_stats2.celery import (app,
                               riot_api,
                               store_get_summoner,
                               store_get_summoners,
                               store_static_get_champion_list,
                               store_static_get_summoner_spell_list,
                               store_get_recent_games,
                               store_get_challenger,
                               store_get_league,
                               store_get_leagues,
                               store_get_match)
from matches.models import MatchDetail

# TODO: Lots of repetition of strings here.
# Consider putting all "store" methods in a class.
# Also, using a single string containing a method name to control flow.

class RiotAPI:
    @staticmethod
    def get_summoner(name=None, region=None):
        func = 'get_summoner'
        kwargs = {'name': name, 'region': region}

        return riot_api.apply_async((func, kwargs),
                                    link=store_get_summoner.s(region=region))

    @staticmethod
    def get_summoners(names=None, ids=None, region=None):
        func = 'get_summoners'
        kwargs = {'names': names, 'ids': ids, 'region': region}

        riot_api.apply_async((func, kwargs),
                             link=store_get_summoners.s(region=region))

    @staticmethod
    def static_get_champion_list(region=None, locale=None, version=None,
                                 data_by_id=None, champ_data=None):
        func = 'static_get_champion_list'
        kwargs = {'region': region, 'locale': locale, 'version': version,
                  'data_by_id': data_by_id, 'champ_data': champ_data}

        riot_api.apply_async((func, kwargs),
                             link=store_static_get_champion_list.s())

    @staticmethod
    def static_get_summoner_spell_list(region=None, locale=None, version=None,
                                       data_by_id=None, spell_data=None):
        func = 'static_get_summoner_spell_list'
        kwargs = {'region': region, 'locale': locale, 'version': version,
                  'data_by_id': data_by_id, 'spell_data': spell_data}

        riot_api.apply_async((func, kwargs),
                             link=store_static_get_summoner_spell_list.s())

    @staticmethod
    def get_recent_games(summoner_id, region=None):
        func = 'get_recent_games'
        kwargs = {'summoner_id': summoner_id, 'region': region}

        riot_api.apply_async((func, kwargs),
                             link=store_get_recent_games.s(summoner_id=summoner_id,
                                                           region=region))

    @staticmethod
    def get_challenger(region=None):
        func = 'get_challenger'
        kwargs = {'region': region}

        riot_api.apply_async((func, kwargs),
                             link=store_get_challenger.s(region=region))

    @staticmethod
    def get_league(summoner_id, region=None):
        """
        Gets a single summoner's league.

        Note: see get_leagues for multiple summoners' leagues.
        """
        func = 'get_league'
        kwargs = {'summoner_ids': [summoner_id], 'region': region}

        riot_api.apply_async((func, kwargs),
                             link=store_get_league.s(summoner_id, region))

    @staticmethod
    def get_leagues(summoner_ids, region=None):
        """
        Gets multiple summoner's league.
        """
        func = 'get_league'
        kwargs = {'summoner_ids': summoner_ids, 'region': region}

        riot_api.apply_async((func, kwargs),
                             link=store_get_leagues.s(summoner_ids, region))

    @staticmethod
    def get_match(match_id, region=None, include_timeline=False):
        """
        Gets a single match, timeline data optionally included.

        Note: Timeline data models not implemented.
        """
        func = 'get_match'
        kwargs = {'match_id': match_id,
                  'region': region,
                  'include_timeline': include_timeline}

        if not MatchDetail.objects.filter(match_id=match_id,
                                          region=region.upper()).exists():
            riot_api.apply_async((func, kwargs),
                                 link=store_get_match.s())

    @staticmethod
    def get_match_history(summoner_id, region=None, champion_ids=None,
                          ranked_queues='RANKED_SOLO_5x5', begin_index=None,
                          end_index=None):
        """
        Gets a range of matches (max 15), based on indices.

        Used to get a list of match IDs to feed into get_match,
        via get_matches_from_ids.
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
            raise ValueError('Unsupported value for "ranked_queues": {};'
                             'use RANKED_SOLO_5x5 or RANKED_TEAM_5x5'
                             .format(ranked_queues))
        else:
            riot_api.apply_async((func, kwargs),
                                 link=get_matches_from_ids.s(region))

@app.task(ignore_result=True)
def get_matches_from_ids(result, region):
    """
    Callback that parses the result dict for match IDs and feeds them back to
    the get_match for getting each match's full dataset (this method's received
    `result` only contains the data for the summoner ID that was passed to it).

    Returns a count of the matches that were saved (cached match data is not
    fetched).

    Note: Assumes matches are of type 5v5.
    """
    if 'matches' in result:
        for match in result['matches']:
            if not MatchDetail.objects.filter(match_id=match['matchId'],
                                              region=region.upper()).exists():
                RiotAPI.get_match(match['matchId'], region=region, include_timeline=False)