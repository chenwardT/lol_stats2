from django.db.models import Count

from .functions import chunks
from leagues.models import LeagueEntry
from summoners.models import Summoner
from riot_api.wrapper import RiotAPI

_MAX_SUMMONER_IDS_PER_QUERY = 40

def get_league_if_none(summoners=None):
    """
    Accepts an iterable of summoners of the same region.
    """
    if summoners is None:
        raise ValueError('Iterable of summoners required, got None.')

    region = summoners[0].region

    to_query = set()

    for s in summoners:
        if not LeagueEntry.objects.filter(player_or_team_id=s.summoner_id,
                                          league__region=s.region).exists():
            to_query.add(s)

    print('Preparing to query {} summoner IDs.'.format(len(to_query)))

    query_list = []

    for summoner in to_query:
        query_list.append(summoner.summoner_id)

    chunked = []

    for chunk in chunks(query_list, 10):
        chunked.append(chunk)

    print("{} queries will be made to fetch {} summoners' leagues.".format(len(chunked),
                                                                          len(query_list)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in chunked:
            RiotAPI.get_league(group, region)

def get_summoners_from_league_entries(league_entries=None, region=None):
    """
    Queries for chunks of summoners whose IDs are known via LeagueEntry records
    but are not stored in the Summoner table.

    Accepts an iterable of LeagueEntry objects and a region.
    Summoner queries are sent as chunks of at most 40 IDs.
    """

    if league_entries is None:
        raise ValueError('league_entries must not be None.')

    # TODO: Validate input.
    if region is None:
        raise ValueError('region must not be None.')

    to_query = set()

    for le in league_entries:
        if not Summoner.objects.filter(region=le.league.region,
                                       summoner_id=le.player_or_team_id).exists():
            to_query.add(le.player_or_team_id)

    query_list = []

    for player in to_query:
        query_list.append(player)

    chunked = []

    for chunk in chunks(query_list, _MAX_SUMMONER_IDS_PER_QUERY):
        chunked.append(chunk)

    print("{} queries will be made to fetch {} summoners.".format(len(chunked),
                                                                  len(query_list)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in chunked:
            RiotAPI.get_summoners(ids=group, region=region)

# TODO: Allow for list of summoner objects to be passed in.
def get_matches_for_summoners_without_history(summoners=None, region=None,
                                              threshold=1, num_matches=10,
                                              ranked_queues='RANKED_SOLO_5x5'):
    match_count = \
        summoners.annotate(match_cnt=Count('participantidentity'))

    query_list = []

    for summoner in match_count:
        if summoner.match_cnt < threshold:
            query_list.append(summoner)

    print("{} queries will be made to fetch {} matches for each of the "
          "{} summoners.".format(len(query_list) * (num_matches + 1), num_matches,
                                 len(query_list)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for summoner in query_list:
            RiotAPI.get_match_history(summoner.summoner_id, region,
                                      ranked_queues=ranked_queues, end_index=num_matches)
