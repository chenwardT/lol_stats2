from .functions import chunks
from leagues.models import LeagueEntry
from riot_api.wrapper import RiotAPI

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

    for group in chunked:
        RiotAPI.get_leagues(group, region)
