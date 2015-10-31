from celery import chain

from leagues.models import League
from utils.functions import chunks
from riot_api.wrapper import RiotAPI
from lol_stats2.celery import riot_api, store_get_summoners

challenger_leagues = {
    "euw": "Wukong's Lancers",
    "eune": "Riven's Zealots",
    "kr": "Riven's Cutthroats",
    "ru": "Darius's Wizards",
    "br": "Varus's Warmongers",
    "lan": "Riven's Zealots",
    "oce": "Darius's Wizards",
    "las": "Nami's Enforcers",
    "na": "Riven's Cutthroats",
}

for region in challenger_leagues:
    league = League.objects.get(region=region, name=challenger_leagues[region])

    challenger_ids = []

    for entry in league.leagueentry_set.all():
        challenger_ids.append(entry.player_or_team_id)

    chunked_ids = chunks(challenger_ids, 40)

    for chunk in chunked_ids:
        RiotAPI.get_summoners(ids=chunk, region=region)
