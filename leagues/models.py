from django.db import models

# TODO: Cleanup.
class LeagueManager(models.Manager):
    def create_or_update_league(self, attrs, region):
        possibly_extant_league = self.filter(region=region,
                                             queue=attrs['queue'],
                                             name=attrs['name'],
                                             tier=attrs['tier'])
        if possibly_extant_league.exists():
            league = possibly_extant_league[0]
            self.update_league(league, attrs, region)
        else:
            self.create_league(attrs, region)

    # TODO: Factor out creation of entries.
    def create_league(self, attrs, region):
        league = self.create(region=region, queue=attrs['queue'],
                             name=attrs['name'], tier=attrs['tier'])
        for entry in attrs['entries']:
            league.leagueentry_set.create_entry(entry)

    def update_league(self, league, attrs, region):
        for entry in attrs['entries']:
            league.leagueentry_set.create_entry(entry)

class League(models.Model):
    """
    Maps to Riot API League DTO.
    """

    region = models.CharField(max_length=4)     # ex. na
    queue = models.CharField(max_length=32)     # ex. RANKED_SOLO_5x5
    name = models.CharField(max_length=32)      # ex. Orianna's Warlocks
    tier = models.CharField(max_length=12)      # ex. CHALLENGER

    objects = LeagueManager()

    def __str__(self):
        return '[{}] {} {} {}'.format(self.region, self.queue, self.name,
                                      self.tier)

    class Meta:
        unique_together = ('region', 'queue', 'name', 'tier')

class LeagueEntryManager(models.Manager):
    def create_entry(self, attrs):
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
    player_or_team_id = models.CharField(max_length=64)     # ex. TEAM-68594bb0-cce0-11e3-a7cc-782bcb4d1861
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


