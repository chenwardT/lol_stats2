"""
Celery config and task definitions.

To start worker, from lol_stats2 dir:
celery -A lol_stats2 worker -l info

Alternatively, use workers.sh.
"""

import os
import logging

from celery import Celery
from celery.exceptions import MaxRetriesExceededError
from riotwatcher.riotwatcher import (RiotWatcher,
                                     LoLException,
                                     error_400,
                                     error_401,
                                     error_404,
                                     error_429,
                                     error_500,
                                     error_503)
from django_pglocks import advisory_lock
from django.conf import settings

from summoners.models import Summoner
from champions.models import Champion
from spells.models import SummonerSpell
from games.models import Game
from leagues.models import League
from matches.models import MatchDetail

# Currently only used in the event of a 5xx HTTP response code from Riot's API.
RIOT_API_RETRY_DELAY = 1

# Used when a non-API rate limit is in effect (e.g. by some Riot service that their API relies on)
NON_API_LIMIT_RETRY_DELAY = 1

logger = logging.getLogger(__name__)

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_stats2.settings.base')

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

@app.task(bind=True, ignore_result=False, rate_limit='.8/s', max_retries=3,
          default_retry_delay=RIOT_API_RETRY_DELAY)
def riot_api(self, kwargs):
    """
    A rate-limited task that queries the Riot API using a RiotWatcher instance.

    Celery accepts a single rate limit for a task, but Riot expresses
    limits in 2 forms (neither of which can be exceeded):
    10 req / 10 sec
    500 req / 10 min

    Ideally, the limit we give Celery could be .8 req/sec, but testing has shown
    that this doesn't always work.

    This task will retry up to 3 times in the following cases:
     -5xx error, retries in RIOT_API_RETRY_DELAY seconds.
     -429 error, retries based on `Retry-After` header in response.
    """
    logger.debug('kwargs: {}, task ID: {}'.format(kwargs, self.request.id))

    func = getattr(riot_watcher, kwargs['method'])

    if 'region' in kwargs and kwargs['region'] is not None:
        kwargs['region'] = kwargs['region'].lower()

    # Create a copy of kwargs w/o `method` to pass to `func`, as modifying the original
    # `kwargs` breaks task retrying (as would occur if we exceed rate limit, etc).
    non_method_kwargs = kwargs.copy()
    non_method_kwargs.pop('method')

    try:
        result = func(**non_method_kwargs)
    except LoLException as e:
        if e == error_400:
            logger.error('400 error')
        elif e == error_401:
            logger.error('401 error')
        elif e == error_404:
            logger.info('404 error')
        elif e == error_429:
            if 'Retry-After' in e.headers:
                retry_after = int(e.headers['Retry-After'])
                logger.critical('429 error, API rate-limit, retrying in %s sec', retry_after)
                try:
                    raise self.retry(countdown=retry_after)
                except MaxRetriesExceededError as e:
                    logger.error('Max retries exceeded, %s', e)
            else:
                logger.error('429 error, non-API rate limit, retrying in %s sec',
                             NON_API_LIMIT_RETRY_DELAY)
                try:
                    raise self.retry(countdown=NON_API_LIMIT_RETRY_DELAY)
                except MaxRetriesExceededError as e:
                    logger.error('Max retries exceeded, %s', e)
        elif e == error_500:
            logger.error('500 error, retrying in %s sec', RIOT_API_RETRY_DELAY)
            try:
                raise self.retry()
            except MaxRetriesExceededError as e:
                logger.error('Max retries exceeded, %s', e)
        elif e == error_503:
            logger.error('503 error, retrying in %s sec', RIOT_API_RETRY_DELAY)
            try:
                raise self.retry()
            except MaxRetriesExceededError as e:
                logger.error('Max retries exceeded, %s', e)
        else:
            logger.exception('Unhandled LoLException (did riotwatcher get updated?)')
            raise
        result = {}
    except:
        logger.exception('Unhandled exception!')
        raise

    return result


# TODO: Consider renaming these tasks.
# TODO: Can these tasks be put in a class and passed around instead of individually?

# TODO: Seems to not be filling out all data. Fixed?
# Check that Summoners created from Matches are getting their remaining
# data here!
# Also check get_summoner for same.
@app.task(routing_key='store.get_summoners')
def store_summoners(result, region):
    """
    Callback that stores the result of RiotWatcher get_summoners calls.
    """
    logger.debug("result: %s, region: %s", result, region)
    region = region.upper()
    storage_result = {'created': 0, 'updated': 0}

    if result:
        for entry in result:
            logger.debug('using entry: {}: {}'.format(entry, result[entry]))
            potentially_extant_summoner = Summoner.objects.filter(
                summoner_id=result[entry]['id'], region=region)

            if potentially_extant_summoner.exists():
                summoner = potentially_extant_summoner.get()
                logger.debug('potentially_extant_summoner: {}'.format(summoner.__dict__))
                summoner.update(region, result[entry])
                storage_result['updated'] += 1
            else:
                Summoner.objects.create_summoner(region, result[entry])
                storage_result['created'] += 1

    if storage_result['created'] == 0 and storage_result['updated'] == 0:
        logger.warning('No summoners created or updated!')
    else:
        logging.info('Stored {} summoners: {} created, {} updated'.format(
            storage_result['created'] + storage_result['updated'],
            storage_result['created'],
            storage_result['updated']))

    return storage_result


@app.task(ignore_result=True)
def store_champion_list(result):
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

    logger.info('Stored {} champions'.format(len(result['data'])))

    return created


@app.task(ignore_result=True)
def store_summoner_spell_list(result):
    """
    Callback that stores the result of RiotWatcher static_get_summoner_list calls.
    Since there are only a handful of spells, we replace all spells w/the new data.
    """
    lock_id = 'store_spells'

    # Convert values to match model fields.
    for value in result['data'].values():
        value['spell_id'] = value.pop('id')
        value['summoner_level'] = value.pop('summonerLevel')

    spell_objs = list(map(lambda kwargs: SummonerSpell(**kwargs), result['data'].values()))

    with advisory_lock(lock_id) as acquired:
        SummonerSpell.objects.all().delete()
        SummonerSpell.objects.bulk_create(spell_objs)

    logger.info('Stored {} summoner spells'.format(len(result['data'])))


# Unused, as MatchDetail is all we're using for now (ranked games).
# TODO: Use game IDs to get match data.
# This way, you get full participant data, instead of just the 1 player's items, etc.
@app.task
def store_recent_games(result, summoner_id, region):
    """
    Callback that stores the result of RiotWatcher get_recent_games calls.
    """
    for attrs in result['games']:
        # We don't want to duplicate existing games, so compare each
        # by game_id and region.
        if not Game.objects.filter(game_id=attrs['gameId'],
                                   region=region).exists():
            Game.objects.create_game(attrs, summoner_id, region)

    logger.info('Stored {} games'.format(len(result['games'])))


@app.task(ignore_result=True)
def store_challenger(result, region):
    """
    Callback that stores the result of RiotWatcher get_challenger calls.

    Replaces the entirety of the challenger league.
    """
    League.objects.create_or_update_league(result, region)

    logger.info('Stored challenger league for {}'.format(region))


@app.task(routing_key='store.get_league')
def store_league(result, region):
    """
    Callback that stores the result of the RiotWatcher get_league calls.
    `summoner_id` is expected to be the single key of the `result` dict.

    Stores a previously unknown league or replaces the entirety of the
    summoner's league's entries if it was known.
    """
    lock_id = 'store_league'

    with advisory_lock(lock_id) as acquired:
        # Empty dict means that the queried summoner is not in a league.
        if result != {}:
            for summoner_id in result:
                logger.debug('Reading leagues for summoner ID {}'.format(summoner_id))
                for league in result[summoner_id]:
                    League.objects.create_or_update_league(league, region)

                # TODO: This is misleading since we can block updates in update_league
                # based on last_update.
                logger.info('Stored {} leagues for [{}] {}'.format(len(result[summoner_id]),
                                                                   region, summoner_id))
            return True
        else:
            return False


@app.task
def store_match(result):
    """
    Callback that stores the result of RiotWatcher get_match calls.
    Creates instances for MatchDetail and all related models.

    Unlike other storage methods, this method reads (match) ID and region from
    the result dict.

    Note: Timeline data not implemented.
    """
    if result != {}:
        created = MatchDetail.objects.create_match(result)
        logger.info('Stored match {} (create time: {})'.format(created, created.match_date()))
        return True
    else:
        return False
