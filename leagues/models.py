from django.db import models

class League(models.Model):
    """
    Maps to Riot API League DTO.
    """

    region = models.CharField(max_length=4)     # ex. na
    queue = models.CharField(max_length=32)     # ex. RANKED_SOLO_5x5
    name = models.CharField(max_length=32)      # ex. Orianna's Warlocks
    tier = models.CharField(max_length=12)      # ex. CHALLENGER

    def __str__(self):
        return '{} {} {} {}'.format(self.region, self.queue, self.name,
                                    self.tier)

    class Meta:
        unique_together = ('region', 'queue', 'name', 'tier')


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

    # MiniSeries DTO
    series_losses = models.SmallIntegerField(null=True, blank=True)
    series_progress = models.CharField(null=True, blank=True, max_length=5)     # ex. WLLNN
    series_target = models.SmallIntegerField(null=True, blank=True)             # 2 or 3
    series_wins = models.SmallIntegerField(null=True, blank=True)

    league = models.ForeignKey(League)

    def __str__(self):
        return '{} {} - {} ({})'.format(self.league,
                                        self.division,
                                        self.player_or_team_name,
                                        self.league_points)

    class Meta:
        unique_together = ('player_or_team_id', 'league')


