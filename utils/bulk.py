from datetime import timedelta

from django.db.models import Count

from .functions import chunks
from leagues.models import LeagueEntry
from summoners.models import Summoner
from riot_api.wrapper import RiotAPI
from lol_stats2.celery import riot_api

_MAX_SUMMONER_IDS_PER_QUERY = 40


# TODO: re: functions that interact w/riot API and "fill in the blanks":
# Standardize accepted params where possible.


def remote_call_duration():
    return float(riot_api.rate_limit[:-2]) ** -1


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

    print("{} queries will be made to fetch {} summoners' leagues."
          .format(len(chunked), len(query_list)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in chunked:
            RiotAPI.get_league(group, region)


def get_summoners_from_league_entries(league_entries=None, region=None):
    """
    Queries for chunks of summoners whose IDs are known via LeagueEntry records
    but are not stored in the Summoner table.

    Accepts a QuerySet for LeagueEntries from which to extract summoner IDs.
    LeagueEntries are checked for individual players and not teams.
    Summoner queries are sent in chunks of at most 40 IDs.
    """

    if league_entries is None:
        raise ValueError('league_entries must not be None.')

    # TODO: Validate input.
    if region is None:
        raise ValueError('region must not be None.')

    known_summoner_ids = set(Summoner.objects.filter(region=region)
                             .values_list('summoner_id', flat=True))

    league_entry_ids = set(map(int, league_entries
                               .exclude(player_or_team_id__contains='TEAM')
                               .values_list('player_or_team_id', flat=True)))

    to_query = league_entry_ids - known_summoner_ids

    chunked = []

    for chunk in chunks(list(to_query), _MAX_SUMMONER_IDS_PER_QUERY):
        chunked.append(chunk)

    eta = timedelta(seconds=remote_call_duration() * len(chunked))

    print('{} queries will be made to fetch {} summoners.\n'
          'This will take about {}.'.format(len(chunked), len(to_query), eta))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in chunked:
            RiotAPI.get_summoners(ids=group, region=region)


# TODO: Allow for list of summoner objects to be passed in.
def get_matches_for_summoners_without_history(summoners=None, region=None,
                                              threshold=1, num_matches=10,
                                              ranked_queues='RANKED_SOLO_5x5'):
    match_count = summoners.annotate(match_cnt=Count('participantidentity'))

    query_list = []

    for summoner in match_count:
        if summoner.match_cnt < threshold:
            query_list.append(summoner)

    eta = timedelta(seconds=remote_call_duration() * len(query_list) *
                    (num_matches + 1))

    print('{} queries will be made to fetch {} matches for each of the '
          '{} summoners.\nThis will take about {}.'
          .format(len(query_list) * (num_matches + 1), num_matches, len(query_list), eta))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for summoner in query_list:
            RiotAPI.get_match_list(summoner.summoner_id, region, ranked_queues=ranked_queues)


def update_summoners(summoners=None, region=None):
    """
    Accepts an iterable of Summoner objects and fully updates their fields.
    """
    ids = []

    for summoner in summoners:
        ids.append(summoner.summoner_id)

    query_list = []

    for chunk in chunks(ids, 40):
        query_list.append(chunk)

    print("{} queries will be made to update {} summoners.".format(len(query_list),
                                                                   len(ids)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in query_list:
            RiotAPI.get_summoners(ids=group, region=region)


def get_matches_for_leagues(leagues=None, region=None,
                            ranked_queues='RANKED_SOLO_5x5', num_matches=10):
    known_summoners = []
    unknown_summoners = []

    for league in leagues:
        for league_entry in league.leagueentry_set.all():
            summoner_query = Summoner.objects.filter(
                summoner_id=league_entry.player_or_team_id,
                region=region)

            if summoner_query.exists():
                known_summoners.append(summoner_query.get().summoner_id)
            else:
                unknown_summoners.append(league_entry.player_or_team_id)

    print('known_summoners:\n{}'.format(known_summoners))
    print('unknown_summoners:\n{}'.format(unknown_summoners))

    summoner_query_list = []

    for chunk in chunks(unknown_summoners, 40):
        summoner_query_list.append(chunk)

    print('Part 1: Get unknown summoners')
    print('{} queries will be made to fetch {} summoners.'.format(
        len(summoner_query_list),
        len(unknown_summoners)))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for group in summoner_query_list:
            RiotAPI.get_summoners(ids=group, region=region)

    known_summoners.extend(unknown_summoners)

    print('Part 2: Get matches')
    print('At most, {} queries will be made to fetch {} matches.'.format(
        len(known_summoners) * (num_matches + 1),
        len(known_summoners) * num_matches))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for summoner_id in known_summoners:
            RiotAPI.get_match_list(summoner_id, region, ranked_queues=ranked_queues)


def get_leagues_for_summoner_ids(ids=None, region=None):
    chunked_ids = list(chunks(ids, 10))

    eta = timedelta(seconds=remote_call_duration() * len(chunked_ids))

    print('{} queries will be made to fetch {} summoners\' leagues.\n'
          'This will take about {}.'
          .format(len(chunked_ids), len(ids), eta))

    response = input('Proceed? (y/[n])\n')

    if response == 'y':
        for chunk in chunked_ids:
            RiotAPI.get_league(summoner_ids=chunk, region=region)
