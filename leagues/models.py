import logging
from datetime import datetime

import pytz
from django.db import models
from django.db import transaction

from summoners.models import Summoner

logger = logging.getLogger(__name__)

class LeagueManager(models.Manager):
    def create_or_update_league(self, attrs, region):

        possibly_extant_league = self.filter(region=region,
                                             queue=attrs['queue'],
                                             name=attrs['name'],
                                             tier=attrs['tier'])
        # TODO: Fine-tune this transaction!
        with transaction.atomic():
            if possibly_extant_league.exists():
                league = possibly_extant_league.get()
                return self.update_league(league, attrs, region)
            else:
                return self.create_league(attrs, region)

    def create_league(self, attrs, region):
        league = self.create(region=region, queue=attrs['queue'],
                             name=attrs['name'], tier=attrs['tier'])
        logger.debug(league)
        league.leagueentry_set.create_entries(attrs)

        return league

    def update_league(self, league, attrs, region):
        logger.debug(league)
        league.leagueentry_set.all().delete()
        league.leagueentry_set.create_entries(attrs)

        return league

class League(models.Model):
    """
    Maps to Riot API League DTO.
    """
    region = models.CharField(max_length=4, db_index=True)     # ex. NA
    queue = models.CharField(max_length=32)     # ex. RANKED_SOLO_5x5
    name = models.CharField(max_length=32)      # ex. Orianna's Warlocks
    tier = models.CharField(max_length=12)      # ex. CHALLENGER

    last_update = models.DateTimeField(auto_now=True)

    objects = LeagueManager()

    def __str__(self):
        return '[{}] {} {} {}'.format(self.region, self.queue, self.name,
                                      self.tier)

    class Meta:
        unique_together = ('region', 'queue', 'name', 'tier')

class LeagueEntryManager(models.Manager):
    def create_entry(self, attrs):
        """
        Create an entry from a dict of format LeagueEntry DTO.

        If the Summoner that this entry refers to is in the database,
        their last_leagues_update field will be updated.

        While Summoners may belong to multiple leagues, and this only refers
        to a single league's entry, all leagues are fetched simultaneously,
        so this is a safe way to trigger updates on last_leagues_update.
        """
        if 'miniSeries' in attrs:
            entry = self.create(division=attrs['division'],
                                is_fresh_blood=attrs['isFreshBlood'],
                                is_hot_streak=attrs['isHotStreak'],
                                is_inactive=attrs['isInactive'],
                                is_veteran=attrs['isVeteran'],
                                league_points=attrs['leaguePoints'],
                                player_or_team_id=attrs['playerOrTeamId'],
                                player_or_team_name=attrs['playerOrTeamName'],
                                wins=attrs['wins'],
                                losses=attrs['losses'],
                                series_losses=attrs['miniSeries']['losses'],
                                series_progress=attrs['miniSeries']['progress'],
                                series_target=attrs['miniSeries']['target'],
                                series_wins=attrs['miniSeries']['wins'])
        else:
            entry = self.create(division=attrs['division'],
                                is_fresh_blood=attrs['isFreshBlood'],
                                is_hot_streak=attrs['isHotStreak'],
                                is_inactive=attrs['isInactive'],
                                is_veteran=attrs['isVeteran'],
                                league_points=attrs['leaguePoints'],
                                player_or_team_id=attrs['playerOrTeamId'],
                                player_or_team_name=attrs['playerOrTeamName'],
                                wins=attrs['wins'],
                                losses=attrs['losses'])

        # If this entry isn't for a team, then update the Summoner's
        # last_leagues_update field.

        # TODO: To ensure the Summoner's last_leagues_update field is not written to
        # multiple times in a short period of time (e.g. when the summoner is in
        # multiple leagues) a time distance check may be performed.
        if 'TEAM' not in attrs['playerOrTeamId']:
            summoner_query = Summoner.objects.filter(
                region=entry.league.region,
                summoner_id=int(attrs['playerOrTeamId']))

            if summoner_query.exists():
                summoner_query.update(last_leagues_update=datetime.now(tz=pytz.utc))
                logger.info('updated last_leagues_update for {}'
                            .format(summoner_query.get()))

        logger.debug(entry)

        return entry

    def create_entries(self, attrs):
        for entry in attrs['entries']:
            self.create_entry(entry)

class LeagueEntry(models.Model):
    """
    Maps to Riot API LeagueEntry DTO.

    Child of League model (many-to-one).

    A summoner ID can be filtered by with this model's manager to get their
    solo queue entry.
    """
    division = models.CharField(max_length=3)               # ex. IV
    is_fresh_blood = models.BooleanField()
    is_hot_streak = models.BooleanField()
    is_inactive = models.BooleanField()
    is_veteran = models.BooleanField()
    league_points = models.IntegerField()

    # TODO: Consider generic association to Summoner/Team or a nullable FK for
    # each.
    player_or_team_id = models.CharField(max_length=64, db_index=True)     # ex. TEAM-68594bb0-cce0-11e3-a7cc-782bcb4d1861
    player_or_team_name = models.CharField(max_length=24)   # ex. Smiteless Baron
    wins = models.IntegerField()
    losses = models.IntegerField()

    # MiniSeries DTO
    series_losses = models.SmallIntegerField(null=True, blank=True)
    series_progress = models.CharField(null=True, blank=True, max_length=5)     # ex. WLLNN
    series_target = models.SmallIntegerField(null=True, blank=True)             # 2 or 3
    series_wins = models.SmallIntegerField(null=True, blank=True)

    league = models.ForeignKey(League)

    objects = LeagueEntryManager()

    def __str__(self):
        return '<{}> {}: {} ({})'.format(self.league,
                                        self.division,
                                        self.player_or_team_name,
                                        self.league_points)

    class Meta:
        unique_together = ('player_or_team_id', 'league')


