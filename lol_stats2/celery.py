import os

from celery import Celery
from riotwatcher.riotwatcher import RiotWatcher

from summoners.models import Summoner
from champions.models import Champion

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_stats2.settings.base')

from django.conf import settings

app = Celery('lol_stats2',
             broker='amqp://',
             backend='amqp://')

# Using a string here means the worker will not have to pickle the object
# when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

riot_watcher = RiotWatcher(os.environ['RIOT_API_KEY'])

@app.task
def riot_api(fn, args):
    """
    A rate-limited task that queries the Riot API using a RiotWatcher instance.
    """
    func = getattr(riot_watcher, fn)
    return func(**args)

# This rate limit results in the greatest common multiple of the 2 stated rate limits:
# 10 req / 10 sec
# 500 req / 10 min
app.control.rate_limit('lol_stats2.celery.riot_api', '50/m')

# TODO: Can these tasks be put in a class and passed around instead of individually?
@app.task
def store_get_summoner(result, region):
    """
    Stores the result of RiotWatcher get_summoner calls.
    See `link` argument of riot_api call in RiotAPI.get_summoner.

    Returns the created/updated Summoner object.
    """
    query = Summoner.objects.filter(region=region, summoner_id=result['id'])

    if not query.exists():
        # Create
        summoner = Summoner.objects.create_summoner(region, result)
    else:
        # Update
        summoner = query[0]
        summoner.update_summoner(region, result)

    return summoner

@app.task
def store_static_get_champion_list(result):
    """
    Stores the result of RiotWatcher static_get_champion_list calls.
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
