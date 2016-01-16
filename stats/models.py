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
