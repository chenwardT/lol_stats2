import logging
from datetime import datetime, timedelta

import pytz
from django.db import models
from django.db import transaction

from summoners.models import Summoner
from utils.functions import underscore_dict

logger = logging.getLogger(__name__)


class LeagueManager(models.Manager):
    def create_or_update_league(self, attrs, region):
        region = region.upper()
        logger.debug('region: %s, attrs: %s', region, attrs)
        possibly_extant_league = self.filter(region=region,
                                             queue=attrs['queue'],
                                             name=attrs['name'],
                                             tier=attrs['tier'])

        if possibly_extant_league.exists():
            league = possibly_extant_league.get()
            return self.update_league(league, attrs)
        else:
            return self.create_league(attrs, region)

    def create_league(self, attrs, region):
        league = self.create(region=region, queue=attrs['queue'],
                             name=attrs['name'], tier=attrs['tier'])
        logger.debug(league)
        league.leagueentry_set.create_entries(attrs)

        return league

    # TODO: Allow timedelta to be passed in.
    @staticmethod
    def update_league(league, attrs):
        if league.last_update < (datetime.now(tz=pytz.utc) - timedelta(seconds=1)):
            logger.debug(league)
            league.last_update = datetime.now(tz=pytz.utc)
            league.save()
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
        get_latest_by = 'last_update'


class LeagueEntryManager(models.Manager):
    @staticmethod
    def _flatten_entry_if_series(entry):
        if 'mini_series' not in entry:
            return entry
        else:
            flattened = entry.copy()

            # We rename the keys in mini_series so they don't conflict w/extant keys.
            renamed_series = entry['mini_series']
            renamed_series['series_losses'] = renamed_series.pop('losses')
            renamed_series['series_wins'] = renamed_series.pop('wins')
            renamed_series['series_progress'] = renamed_series.pop('progress')
            renamed_series['series_target'] = renamed_series.pop('target')

            # Merge the series in and remove the original that has since been renamed.
            flattened.update(renamed_series)
            flattened.pop('mini_series')

            return flattened

    def create_entries(self, attrs):
        entries = attrs['entries']
        underscore_entries = [entry for entry in map(underscore_dict, entries)]
        flattened_entries = [entry for entry in map(self._flatten_entry_if_series, underscore_entries)]

        # `instance` contains the League object that we called `leagueentry_set` on.
        for entry in flattened_entries:
            entry['league_id'] = self.instance.id

        entry_objs = [LeagueEntry(**kwargs) for kwargs in flattened_entries]
        self.bulk_create(entry_objs)

        logger.debug('Bulk created {} league entries'.format(len(flattened_entries)))


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


