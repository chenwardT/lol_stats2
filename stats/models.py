from django.db import models, transaction
from django.apps import apps

# TODO: Manage least-significant version field, i.e. ability to merge 5.2.0.22, 5.2.0.46, etc
class Bucket(models.Model):
    """
    A bucket contains filters that apply to all champions that are analyzed.
    Each of version, lane, role, and region may be 'ALL' to signify a result
    calculated without filtering on that version, lane, role, or region, respectively.

    See utils.constants for valid values.
    """
    version = models.CharField(max_length=16)     # ex. '5.22.0.345', 'ALL'
    is_exact_version = models.BooleanField()      # See utils.functions.is_complete_version
    region = models.CharField(max_length=8)       # ex. 'EUW', 'ALL'
    lane = models.CharField(max_length=16)
    role = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('version', 'region', 'lane', 'role')

    def __str__(self):
        return '[{}] V:{} L:{} R:{}'.format(self.region, self.version, self.lane, self.role)

class ChampionStatsManager(models.Manager):
    # TODO: Compare perf w/postgres 9.5 UPSERT (not used by Django yet)
    def upsert(self, lane, role, version, is_exact_version, region, champion_id, update_fields):
        """
        Accepts parameters specifying a Bucket, ChampionStats object, and a
        dict of fields to update along with their respective values.
        If the Bucket or ChampionStats objects don't exist, they are created.

        Returns the updated ChampionStats object.
        """
        with transaction.atomic():
            bucket = Bucket.objects.get_or_create(lane=lane,
                                                  role=role,
                                                  version=version,
                                                  is_exact_version=is_exact_version,
                                                  region=region)[0]
            champ_stats_obj = bucket.championstats_set.update_or_create(champion_id=champion_id,
                                                                        defaults=update_fields)
            return champ_stats_obj[0]

class ChampionStats(models.Model):
    # "rate" fields are intended to be expressed as a percentage.
    bucket = models.ForeignKey(Bucket)
    champion_id = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    
    sum_picks = models.BigIntegerField(blank=True, null=True)
    sum_bans = models.BigIntegerField(blank=True, null=True)
    sum_wins = models.BigIntegerField(blank=True, null=True)
    win_rate = models.FloatField(blank=True, null=True)
    # Useful for checking integrity?
    sum_losses = models.BigIntegerField(blank=True, null=True)
    pick_rate = models.FloatField(blank=True, null=True)
    # Averaged count of times picked by all players.
    avg_pick_count = models.FloatField(blank=True, null=True)
    sum_kills = models.BigIntegerField(blank=True, null=True)
    avg_kills = models.FloatField(blank=True, null=True)
    sum_deaths = models.BigIntegerField(blank=True, null=True)
    avg_death = models.FloatField(blank=True, null=True)
    sum_assists = models.BigIntegerField(blank=True, null=True)
    avg_assists = models.FloatField(blank=True, null=True)
    sum_largest_killing_spree = models.BigIntegerField(blank=True, null=True)
    avg_largest_killing_spree = models.FloatField(blank=True, null=True)
    sum_damage_dealt = models.BigIntegerField(blank=True, null=True)
    avg_damage_dealt = models.FloatField(blank=True, null=True)
    sum_damage_taken = models.BigIntegerField(blank=True, null=True)
    avg_damage_taken = models.FloatField(blank=True, null=True)
    # Double-check these for self vs all healing
    sum_self_healing = models.BigIntegerField(blank=True, null=True)
    avg_self_healing = models.FloatField(blank=True, null=True)
    sum_minions_killed = models.BigIntegerField(blank=True, null=True)
    avg_minions_killed = models.FloatField(blank=True, null=True)
    # CS obtained from enemy jungle
    sum_enemy_jungle_cs = models.BigIntegerField(blank=True, null=True)
    avg_enemy_jungle_cs = models.FloatField(blank=True, null=True)
    # CS obtained from friendly jungle
    sum_team_jungle_cs = models.BigIntegerField(blank=True, null=True)
    avg_team_jungle_cs = models.FloatField(blank=True, null=True)
    sum_gold_earned = models.BigIntegerField(blank=True, null=True)
    avg_gold_earned = models.FloatField(blank=True, null=True)
    # TODO: Develop metrics based on weighting of different stats per role
    # Strongly dependent on win rate.
    role_position = models.IntegerField(blank=True, null=True)
    position_delta = models.IntegerField(blank=True, null=True)

    objects = ChampionStatsManager()

    class Meta:
        unique_together = ['bucket', 'champion_id']

    def __str__(self):
        champion_model = apps.get_model('champions', 'Champion')
        return '[{}] {} V:{}  L:{} R:{}'.format(self.bucket.region,
                                                champion_model.objects.get(champion_id=self.champion_id),
                                                self.bucket.version,
                                                self.bucket.lane,
                                                self.bucket.role)