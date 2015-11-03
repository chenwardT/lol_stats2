"""
Celery config and task definitions.

To start worker, from lol_stats2 dir:
celery -A lol_stats2 worker -l info

Alternatively, use workers.sh.
"""

import os
import logging
import time

from celery import Celery, chain, group
from riotwatcher.riotwatcher import (RiotWatcher,
                                     LoLException,
                                     error_400,
                                     error_401,
                                     error_404,
                                     error_429,
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
# TODO: Create separate task for static API calls (not counted against rate limit).

# TODO: Refine parameters for retrying: read that new response header for when we can retry!
# FIXME: Params
@app.task(bind=True, ignore_result=False, rate_limit='.5/s', max_retries=3,
          default_retry_delay=2)
def riot_api(self, kwargs):
    """
    A rate-limited task that queries the Riot API using a RiotWatcher instance.

    Celery accepts a single rate limit for a task, but Riot expresses
    limits in 2 forms (neither of which can be exceeded):
    10 req / 10 sec
    500 req / 10 min

    Ideally, the limit we give Celery could be .8 req/sec, but testing has shown
    that anything over .5 req/sec is prone to hitting HTTP 429 errors.

    If an LoLException is thrown, automatically retries up to 3 times,
    with a 2 second delay between each attempt.
    """

    logger.debug('kwargs: {}, task ID: {}'.format(kwargs, self.request.id))
    func = getattr(riot_watcher, kwargs.pop('method'))

    if 'region' in kwargs:
        kwargs['region'] = kwargs['region'].lower()

    # Note: Preventing exceptions from propagating hides them from flower.
    # Exceptions of type `retry` will however, be shown.
    try:
        result = func(**kwargs)
    except LoLException as e:
        if e == error_500 or e == error_503:
            logger.error('5xx error, retrying ({})'.format(e))
            raise self.retry(exc=e)
        elif e == error_429:
            logger.error('429 error, retrying ({})'.format(e))
            raise self.retry(exc=e)
        else:
            logger.error('Unexpected error, retrying ({})'.format(e))
        result = {}
    except:
        logger.error('Unhandled exception', exc_info=True)
        raise

    return result


# TODO: Consider renaming these tasks.
# TODO: Can these tasks be put in a class and passed around instead of individually?

# TODO: Seems to not be filling out all data. Fixed?
# Check that Summoners created from Matches are getting their remaining
# data here!
# Also check get_summoner for same.
@app.task(routing_key='store.get_summoners')
def store_get_summoners(result, region):
    """
    Callback that stores the result of RiotWatcher get_summoners calls.
    """
    region = region.upper()
    updated = 0
    created = 0

    for entry in result:
        logger.debug(entry)
        potentially_extant_summoner = Summoner.objects.filter(
            summoner_id=result[entry]['id'], region=region)

        if potentially_extant_summoner.exists():
            summoner = potentially_extant_summoner.get()
            summoner.update(region, result[entry])
            updated += 1
        else:
            Summoner.objects.create_summoner(region, result[entry])
            created += 1

    if updated == 0 and created == 0:
        logger.warning('No summoners updated or created!')
    else:
        logging.info('Got {} summoners, {} updated, {} created'.format(
            updated + created, updated, created))


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

    logger.info('Got {} champions'.format(len(result['data'])))

    return created


# TODO: In testing, when this got ran repeatedly in a short period of time,
# it looks like they can be run in parallel (we don't want that) as shown by
# IntegrityError exceptions.
@app.task(ignore_result=True)
def store_static_get_summoner_spell_list(result):
    """
    Callback that stores the result of RiotWatcher static_get_summoner_list calls.
    Since there are only a handful of spells, we replace all spells w/the new data.
    """
    SummonerSpell.objects.all().delete()

    for attrs in result['data'].values():
        SummonerSpell.objects.create_spell(attrs)

    logger.info('Got {} summoner spells'.format(len(result['data'])))


# Unused, as MatchDetail is all we're using for now (ranked games).
# TODO: Use game IDs to get match data.
# This way, you get full participant data, instead of just the 1 player's items, etc.
@app.task
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

    logger.info('Got {} games'.format(len(result['games'])))


@app.task(ignore_result=True)
def store_get_challenger(result, region):
    """
    Callback that stores the result of RiotWatcher get_challenger calls.

    Replaces the entirety of the challenger league.
    """
    League.objects.create_or_update_league(result, region)

    logger.info('Updated challenger league for {}'.format(region))


@app.task(routing_key='store.get_league')
def store_get_league(result, region):
    """
    Callback that stores the result of the RiotWatcher get_league calls.
    `summoner_id` is expected to be the single key of the `result` dict.

    Stores a previously unknown league or replaces the entirety of the
    summoner's league's entries if it was known.
    """
    # TODO: Fix IntegrityError, duplicate player_or_team_id + league_id.

    # Empty dict means that the queried summoner is not in a league.
    if result != {}:
        for id in result:
            logger.debug('Reading leagues for summoner ID {}'.format(id))
            for league in result[id]:
                League.objects.create_or_update_league(league, region)

            logger.info('Got {} leagues for [{}] {}'.format(
                len(result[id]), region, id))


@app.task
def store_get_match(result):
    """
    Callback that stores the result of RiotWatcher get_match calls.
    Creates instances for MatchDetail and all related models.

    Unlike other storage methods, this method reads (match) ID and region from
    the result dict.

    Note: Timeline data not implemented.
    """
    if result != {}:
        created = MatchDetail.objects.create_match(result)

        logger.info('Got match {}'.format(created))
