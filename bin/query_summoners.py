import os
import time

from django.db import IntegrityError
from riotwatcher.riotwatcher import RiotWatcher, NORTH_AMERICA

# from lol_stats2.settings.development import get_env_variable
from utils.utility_functions import chunks
from summoners.models import Summoner

MAX_IDS_PER_QUERY = 40

rw = RiotWatcher(os.environ['RIOT_API_KEY'])
print(rw.can_make_request())

summoner_ids = []

with open('../seed/summonerIds.txt', 'r') as f:
    summoner_ids = f.readlines()

summoner_ids = [int(id.strip('\n')) for id in summoner_ids]
print("Summoner IDs to query: {}".format(summoner_ids))
chunked_ids = list(chunks(summoner_ids, MAX_IDS_PER_QUERY))

for chunk in chunked_ids:
    while not rw.can_make_request():
        time.sleep(1)

    summoners = rw.get_summoners(ids=chunk, region=NORTH_AMERICA)

    for k in summoners:
        try:
            Summoner.objects.create_summoner(NORTH_AMERICA, summoners[k])
        except IntegrityError as e:
            print(e)