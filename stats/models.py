from django.db import models, transaction
from django.apps import apps

# TODO: Manage least-significant version field, i.e. ability to merge 5.2.0.22, 5.2.0.46, etc
class Bucket(models.Model):
    """
    A bucket contains filters that apply to all champions that are analyzed.
    Each of version, lane, role, and region may be 'ALL' to signify a result
    calculated without filtering on that version, lane, role, or region, respectively.

    Known combinations of (LANE, ROLE):

    ('BOTTOM', 'DUO')
    ('BOTTOM', 'DUO_CARRY')
    ('BOTTOM', 'DUO_SUPPORT')
    ('BOTTOM', 'NONE')
    ('BOTTOM', 'SOLO')
    ('JUNGLE', 'NONE')
    ('MIDDLE', 'DUO')
    ('MIDDLE', 'DUO_CARRY')
    ('MIDDLE', 'DUO_SUPPORT')
    ('MIDDLE', 'NONE')
    ('MIDDLE', 'SOLO')
    ('TOP',    'DUO')
    ('TOP',    'DUO_CARRY')
    ('TOP',    'DUO_SUPPORT')
    ('TOP',    'NONE')
    ('TOP',    'SOLO')
    """
    version = models.CharField(max_length=16)     # ex. '5.22.0.345', 'ALL'
    region = models.CharField(max_length=8)       # ex. 'EUW', 'ALL'
    lane = models.CharField(max_length=16)
    role = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('version', 'region', 'lane', 'role')

class ChampionStatsManager(models.Manager):
    # TODO: Compare perf w/postgres 9.5 UPSERT (not used by Django yet)
    def upsert(self, lane, role, version, region, champion_id, update_fields):
        with transaction.atomic():
            bucket = Bucket.objects.get_or_create(lane=lane,
                                                  role=role,
                                                  version=version,
                                                  region=region)[0]
            champ_stats_obj = bucket.championstats_set.update_or_create(champion_id=champion_id,
                                                                        defaults=update_fields)
            return champ_stats_obj[0]

class ChampionStats(models.Model):
    bucket = models.ForeignKey(Bucket)
    champion_id = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    
    total_picks = models.BigIntegerField(blank=True, null=True)
    total_bans = models.BigIntegerField(blank=True, null=True)
    total_wins = models.BigIntegerField(blank=True, null=True)
    win_rate = models.IntegerField(blank=True, null=True)
    # Useful for checking integrity?
    total_losses = models.BigIntegerField(blank=True, null=True)
    pick_rate = models.IntegerField(blank=True, null=True)
    # Averaged count of times picked by all players.
    avg_pick_count = models.IntegerField(blank=True, null=True)
    total_kills = models.BigIntegerField(blank=True, null=True)
    avg_kills = models.IntegerField(blank=True, null=True)
    total_deaths = models.BigIntegerField(blank=True, null=True)
    avg_death = models.IntegerField(blank=True, null=True)
    total_assists = models.BigIntegerField(blank=True, null=True)
    avg_assists = models.IntegerField(blank=True, null=True)
    total_killing_sprees = models.BigIntegerField(blank=True, null=True)
    avg_largest_killing_spree = models.IntegerField(blank=True, null=True)
    total_damage_dealt = models.BigIntegerField(blank=True, null=True)
    avg_damage_dealt = models.IntegerField(blank=True, null=True)
    total_damage_taken = models.BigIntegerField(blank=True, null=True)
    avg_damage_taken = models.IntegerField(blank=True, null=True)
    # Double-check these for self vs all healing
    total_self_healing = models.BigIntegerField(blank=True, null=True)
    avg_self_healing = models.IntegerField(blank=True, null=True)
    total_minions_killed = models.BigIntegerField(blank=True, null=True)
    avg_minions_killed = models.IntegerField(blank=True, null=True)
    # CS obtained from enemy jungle
    total_enemy_jungle_cs = models.BigIntegerField(blank=True, null=True)
    avg_enemy_jungle_cs = models.IntegerField(blank=True, null=True)
    # CS obtained from friendly jungle
    total_team_jungle_cs = models.BigIntegerField(blank=True, null=True)
    avg_team_jungle_cs = models.IntegerField(blank=True, null=True)
    total_gold_earned = models.BigIntegerField(blank=True, null=True)
    avg_gold_earned = models.IntegerField(blank=True, null=True)
    # TODO: Develop metrics based on weighting of different stats per role
    #       Strongly dependent on win rate.
    role_position = models.IntegerField(blank=True, null=True)
    position_delta = models.IntegerField(blank=True, null=True)

    objects = ChampionStatsManager()

    def __str__(self):
        champion_model = apps.get_model('champions', 'Champion')
        return '{} {} {} {} {}'.format(self.bucket.region,
                                       self.bucket.version,
                                       champion_model.objects.get(champion_id=self.champion_id),
                                       self.bucket.lane,
                                       self.bucket.role)