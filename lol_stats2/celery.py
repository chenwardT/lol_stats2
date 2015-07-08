"""
Celery config and task definitions.

To start worker, from lol_stats2 dir:
celery -A lol_stats2 worker -l info
"""

import os
import logging

from celery import Celery
from riotwatcher.riotwatcher import (RiotWatcher,
                                     LoLException,
                                     error_404,
                                     error_500,
                                     error_503)

from summoners.models import Summoner
from champions.models import Champion
from spells.models import SummonerSpell
from games.models import Game
from leagues.models import League
from matches.models import MatchDetail

logger = logging.getLogger(__name__)

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_stats2.settings.base')

from django.conf import settings

app = Celery('lol_stats2',
             broker='amqp://',
             backend='redis://'
             )

# Using a string here means the worker will not have to pickle the object
# when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

riot_watcher = RiotWatcher(os.environ['RIOT_API_KEY'])

# TODO: Move tasks into separate modules.
# TODO: Use self.retry(), in cases where Riot servers could return 5xx.

# TODO: Create separate task for static API calls (not counted against rate limit).
@app.task(bind=True, ignore_result=False)
def riot_api(self, fn, args):
    """
    A rate-limited task that queries the Riot API using a RiotWatcher instance.
    """
    func = getattr(riot_watcher, fn)

    print('riot_api fn: {}, args: {}'.format(fn, args))

    if 'region' in args:
        args['region'] = args['region'].lower()

    try:
        result = func(**args)
    except LoLException as e:
        print(e)
        # TODO: Test this.
        if e == error_500 or e == error_503:
            print('5xx error, retrying ({})'.format(e))
            raise self.retry(exc=e)
        result = {}

    return result

# This rate limit results in the greatest common multiple of the 2 stated rate limits:
# 10 req / 10 sec
# 500 req / 10 min
# ...and tuned down a bit due to inconsistencies between our timing and Riot's.
app.control.rate_limit('lol_stats2.celery.riot_api', '.6/s')

# TODO: Consider renaming these tasks.
# TODO: Can these tasks be put in a class and passed around instead of individually?
@app.task(routing_key='store.get_summoner')
def store_get_summoner(result, region):
    """
    Callback that stores the result of RiotWatcher get_summoner calls.
    See `link` argument of riot_api call in RiotAPI.get_summoner.

    Returns the created/updated Summoner object.
    """
    query = Summoner.objects.filter(region=region, summoner_id=result['id'])

    if not query.exists():
        summoner = Summoner.objects.create_summoner(region, result)
    else:
        summoner = query[0]
        summoner.update(region, result)

    return summoner

@app.task(ignore_result=True)
def store_get_summoners(result, region):
    """
    Callback that stores the result of RiotWatcher get_summoners calls.
    """
    for summoner_id in result:
        potentially_extant_summoner = Summoner.objects.filter(
            summoner_id=summoner_id, region=region)

        if potentially_extant_summoner.exists():
            summoner = potentially_extant_summoner[0]
            summoner.update(region, result[summoner_id])
        else:
            Summoner.objects.create_summoner(region, result[summoner_id])

@app.task(ignore_result=True)
def store_static_get_champion_list(result):
    """
    Callback that stores the result of RiotWatcher static_get_champion_list calls.
    See `link` argument of riot_api call in RiotAPI.static_get_champion_list.

    Returns a list of Champion objects added (None if no additions).
    """
    query = Champion.objects.all()

    created = []

    if not query.exists():
        # This must be a DB initialization, since the table is empty.
        for attrs in result['data'].values():
            created.append(Champion.objects.create_champion(attrs))
    else:
        # We have some champions in the DB, so we will only need to add new ones.
        for attrs in result['data'].values():
            # Compare by ID
            if not Champion.objects.filter(champion_id=attrs['id']).exists():
                created.append(Champion.objects.create_champion(attrs))

    return created

# TODO: In testing, when this got ran repeatedly in a short period of time,
# it looks like they can be run in parallel (we don't want that) as shown by
# IntegrityError exceptions.
# One solution: locking DB when any of these types of tasks run.
@app.task(ignore_result=True)
def store_static_get_summoner_spell_list(result):
    """
    Callback that stores the result of RiotWatcher static_get_summoner_list calls.
    Since there are only a handful of spells, we replace all spells w/the new data.
    """
    SummonerSpell.objects.all().delete()

    for attrs in result['data'].values():
        SummonerSpell.objects.create_spell(attrs)

# TODO: Use game IDs to get match data.
# This way, you get full participant data, instead of just the 1 player's items, etc.
# Note: This is unused as MatchDetail is all we're using for now (ranked games).
@app.task(ignore_result=True)
def store_get_recent_games(result, summoner_id, region):
    """
    Callback that stores the result of RiotWatcher get_recent_games calls.
    """
    for attrs in result['games']:
        # We don't want to duplicate existing games, so compare each
        # by game_id and region.
        if not Game.objects.filter(game_id=attrs['gameId'],
                                   region=region).exists():
            Game.objects.create_game(attrs, summoner_id, region)

@app.task(ignore_result=True)
def store_get_challenger(result, region):
    """
    Callback that stores the result of RiotWatcher get_challenger calls.

    Replaces the entirety of the challenger league.
    """
    League.objects.create_or_update_league(result, region)

# TODO: If a summoner is in multiple leagues, e.g. they are on 2+ teams,
# or plays 3s and 5s, there will be multiple entries in the list,
# so using [0] is unsound.

@app.task(ignore_result=True, routing_key='store.get_league')
def store_get_league(result, summoner_id, region):
    """
    Callback that stores the result of the RiotWatcher get_league calls.
    `summoner_id` is expected to be the single key of the `result` dict.

    Stores a previously unknown league or replaces the entirety of the
    summoner's league's entries if it was known.
    """
    # TODO: Fix IntegrityError, duplicate player_or_team_id + league_id.
    # Empty dict means that the queried summoner is not in a league.
    if result != {}:
        League.objects.create_or_update_league(result[str(summoner_id)][0], region)

@app.task(ignore_result=True, routing_key='store.get_leagues')
def store_get_leagues(result, summoner_ids, region):
    """
    Callback that stores the result of the RiotWatcher get_league calls.
    `summoner_id` is expected to be the single key of the `result` dict.

    Stores a previously unknown league or replaces the entirety of the
    summoner's league's entries if it was known.
    """
    # TODO: Fix IntegrityError, duplicate player_or_team_id + league_id.
    # Empty dict means that the queried summoner is not in a league.
    if result != {}:
        for key in result:
                League.objects.create_or_update_league(result[str(key)][0], region)

@app.task(ignore_result=True)
def store_get_match(result):
    """
    Callback that stores the result of RiotWatcher get_match calls.
    Creates instances for MatchDetail and all related models.

    Unlike other storage methods, this method reads (match) ID and region from
    the result dict.

    Note: Timeline data not implemented.
    """
    if result != {}:
        MatchDetail.objects.create_match(result)

# @app.task
# def store_get_match_history(result, region):
#     """
#     Callback that parses the result dict for match IDs and feeds them back to
#     the wrapper for getting each match's full dataset (this method's received
#     `result` only contains the data for the summoner ID that was passed to it).
#
#     Note: Assumes matches are of type 5v5.
#     """
#
#     match_ids = []
#
#     for match in result['matches']:
#         match_ids.append(match['matchId'])
#
#     for match_id in match_ids:
#         RiotAPI.get_match(match_id, region=region, include_timeline=False)