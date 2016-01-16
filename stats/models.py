from django.db import models


class Bucket(models.Model):
    # TODO: Manage least-significant version field, i.e. ability to merge 5.2.0.22, 5.2.0.46, etc
    version = models.CharField(max_length=16)     # ex. '5.22.0.345', 'ALL'
    region = models.CharField(max_length=8)       # ex. 'NA', 'EUW'
    lane = models.CharField(max_length=16)        # ex. 'BOTTOM'
    role = models.CharField(max_length=16)        # ex. 'DUO_SUPPORT'
    created_at = models.DateTimeField(auto_now_add=True)


class ChampionStats(models.Model):
    bucket = models.ForeignKey(Bucket)
    champion_id = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    pick_count = models.BigIntegerField()
    ban_count = models.BigIntegerField()
    win_count = models.BigIntegerField()
    win_rate = models.IntegerField()
    # Useful for checking integrity?
    loss_count = models.BigIntegerField()
    pick_rate = models.IntegerField()
    # Averaged count of times picked by all players.
    avg_pick_count = models.IntegerField()
    total_kills = models.BigIntegerField()
    avg_kills = models.IntegerField()
    total_deaths = models.BigIntegerField()
    avg_death = models.IntegerField()
    total_assists = models.BigIntegerField()
    avg_assists = models.IntegerField()
    total_killing_sprees = models.BigIntegerField()
    avg_largest_killing_spree = models.IntegerField()
    total_damage_dealt = models.BigIntegerField()
    avg_damage_dealt = models.IntegerField()
    total_damage_taken = models.BigIntegerField()
    avg_damage_taken = models.IntegerField()
    # Double-check these for self vs all healing
    total_self_healing = models.BigIntegerField()
    avg_self_healing = models.IntegerField()
    total_minions_killed = models.BigIntegerField()
    avg_minions_killed = models.IntegerField()
    # CS obtained from enemy jungle
    total_enemy_jungle_cs = models.BigIntegerField()
    avg_enemy_jungle_cs = models.IntegerField()
    # CS obtained from friendly jungle
    total_team_jugnle_cs = models.BigIntegerField()
    avg_team_jungle_cs = models.IntegerField()
    total_gold_earned = models.BigIntegerField()
    avg_gold_earned = models.IntegerField()
    # TODO: Develop metrics based on weighting of different stats per role
    #       Strongly dependent on win rate.
    role_position = models.IntegerField()
    position_delta = models.IntegerField()