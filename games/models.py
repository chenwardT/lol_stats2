import time
import logging

from django.db import models

from summoners.models import Summoner
from champions.models import Champion
from spells.models import SummonerSpell

logger = logging.getLogger(__name__)

class Player(models.Model):
    """
    Maps to Riot API fellowPlayer DTO. game-v1.3.

    fellowPlayer is related to match history query.
    """
    champion = models.ForeignKey(Champion)
    summoner = models.ForeignKey(Summoner)
    team_id = models.IntegerField()     # 100, 200
    game = models.ForeignKey('Game')

    class Meta:
        ordering = ('team_id',)

    def __str__(self):
        return '%s on %s (Team %d)' % (self.summoner, self.champion, self.team_id)

    def region(self):
        return self.participant_of.region


class RawStat(models.Model):
    """
    Maps to Riot API RawStats DTO, game-v1.3.

    RawStats is related to match history query.
    """
    assists = models.IntegerField(blank=True, null=True)
    barracks_killed = models.IntegerField(blank=True, null=True)
    champions_killed = models.IntegerField(blank=True, null=True)
    combat_player_score = models.IntegerField(blank=True, null=True)
    consumables_purchased = models.IntegerField(blank=True, null=True)
    damage_dealt_player = models.IntegerField(blank=True, null=True)
    double_kills = models.IntegerField(blank=True, null=True)
    first_blood = models.IntegerField(blank=True, null=True)
    gold = models.IntegerField(blank=True, null=True)
    gold_earned = models.IntegerField(blank=True, null=True)
    gold_spent = models.IntegerField(blank=True, null=True)
    item0 = models.IntegerField(blank=True, null=True)
    item1 = models.IntegerField(blank=True, null=True)
    item2 = models.IntegerField(blank=True, null=True)
    item3 = models.IntegerField(blank=True, null=True)
    item4 = models.IntegerField(blank=True, null=True)
    item5 = models.IntegerField(blank=True, null=True)
    item6 = models.IntegerField(blank=True, null=True)
    items_purchased = models.IntegerField(blank=True, null=True)
    killing_sprees = models.IntegerField(blank=True, null=True)
    largest_critical_strike = models.IntegerField(blank=True, null=True)
    largest_killing_spree = models.IntegerField(blank=True, null=True)
    largest_multi_kill = models.IntegerField(blank=True, null=True)
    legendary_items_created = models.IntegerField(blank=True, null=True)  # Number of tier 3 items built.
    level = models.IntegerField(blank=True, null=True)
    magic_damage_dealt_player = models.IntegerField(blank=True, null=True)
    magic_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    magic_damage_taken = models.IntegerField(blank=True, null=True)
    minions_denied = models.IntegerField(blank=True, null=True)
    minions_killed = models.IntegerField(blank=True, null=True)
    neutral_minions_killed = models.IntegerField(blank=True, null=True)
    neutral_minions_killed_enemy_jungle = models.IntegerField(blank=True, null=True)
    neutral_minions_killed_your_jungle = models.IntegerField(blank=True, null=True)
    nexus_killed = models.NullBooleanField(blank=True, null=True)  # Flag specifying if the summoner got the killing blow on the nexus.
    node_capture = models.IntegerField(blank=True, null=True)
    node_capture_assist = models.IntegerField(blank=True, null=True)
    node_neutralize = models.IntegerField(blank=True, null=True)
    node_neutralize_assist = models.IntegerField(blank=True, null=True)
    num_deaths = models.IntegerField(blank=True, null=True)
    num_items_bought = models.IntegerField(blank=True, null=True)
    objective_player_score = models.IntegerField(blank=True, null=True)
    penta_kills = models.IntegerField(blank=True, null=True)
    physical_damage_dealt_player = models.IntegerField(blank=True, null=True)
    physical_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    physical_damage_taken = models.IntegerField(blank=True, null=True)
    player_position = models.IntegerField(blank=True, null=True)
    player_role = models.IntegerField(blank=True, null=True)
    quadra_kills = models.IntegerField(blank=True, null=True)
    sight_wards_bought = models.IntegerField(blank=True, null=True)
    spell_1_cast = models.IntegerField(blank=True, null=True)  # Number of times first champion spell was cast.
    spell_2_cast = models.IntegerField(blank=True, null=True)  # Number of times second champion spell was cast.
    spell_3_cast = models.IntegerField(blank=True, null=True)  # Number of times third champion spell was cast.
    spell_4_cast = models.IntegerField(blank=True, null=True)  # Number of times fourth champion spell was cast.
    summon_spell_1_cast = models.IntegerField(blank=True, null=True)
    summon_spell_2_cast = models.IntegerField(blank=True, null=True)
    super_monster_killed = models.IntegerField(blank=True, null=True)
    team = models.IntegerField(blank=True, null=True)  # redundant due to Game.team_id
    team_objective = models.IntegerField(blank=True, null=True)
    time_played = models.IntegerField(blank=True, null=True)
    total_damage_dealt = models.IntegerField(blank=True, null=True)
    total_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    total_damage_taken = models.IntegerField(blank=True, null=True)
    total_heal = models.IntegerField(blank=True, null=True)
    total_player_score = models.IntegerField(blank=True, null=True)
    total_score_rank = models.IntegerField(blank=True, null=True)
    total_time_crowd_control_dealt = models.IntegerField(blank=True, null=True)
    total_units_healed = models.IntegerField(blank=True, null=True)
    triple_kills = models.IntegerField(blank=True, null=True)
    true_damage_dealt_player = models.IntegerField(blank=True, null=True)
    true_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    true_damage_taken = models.IntegerField(blank=True, null=True)
    turrets_killed = models.IntegerField(blank=True, null=True)
    unreal_kills = models.IntegerField(blank=True, null=True)
    victory_point_total = models.IntegerField(blank=True, null=True)
    vision_wards_bought = models.IntegerField(blank=True, null=True)
    ward_killed = models.IntegerField(blank=True, null=True)
    ward_placed = models.IntegerField(blank=True, null=True)
    win = models.NullBooleanField(blank=True, null=True)  # Flag specifying whether or not this game was won.

    def __str__(self):
        return 'Stats for %s' % Game.objects.get(stats=self)

    # def __iter__(self):
    #     """Generator that returns field names and values for each value that is not None."""
    #     for i in self._meta.get_all_field_names():
    #         if getattr(self, i) is not None:
    #             yield '{}: {}'.format(inflection.humanize(i), getattr(self, i))

    # def belongs_to(self):
    #     return Game.objects.get(stats=self).summoner_id
    #
    # def champion_played(self):
    #     return Game.objects.get(stats=self).champion_id
    #
    # def game_id(self):
    #     return Game.objects.get(stats=self).game_id
    #
    # def region(self):
    #     return Game.objects.get(stats=self).region

    def timestamp(self):
        return Game.objects.get(stats=self).create_date_str()


class GameManager(models.Manager):
    def create_game(self, attrs, summoner_id, region):
        logger.info("Creating game from: {}".format(attrs))

        game = self.create()


class Game(models.Model):
    """
    Maps to Riot API Game DTO, game-v1.3.

    Instead of summonerId and championId, foreign keys to those objects are used.
    RawStat object is related to by these objects via 1-to-1.
    Player objects point to this to allow reverse-querying of match participants.

    To get a match history (QuerySet), given a region (R) and Summoner name (N):

    Game.objects.filter(summoner_id=Summoner.objects.filter(region=R).filter(name=N)

    Alternatively, given a Summoner object (S):

    S.game_set.all()
    """
    summoner_id = models.ForeignKey(Summoner)
    champion_id = models.ForeignKey(Champion)
    create_date = models.BigIntegerField()
    game_id = models.BigIntegerField()
    game_mode = models.CharField(max_length=16)
    game_type = models.CharField(max_length=16)
    invalid = models.BooleanField()
    ip_earned = models.IntegerField()
    level = models.IntegerField()
    map_id = models.IntegerField()
    spell_1 = models.IntegerField()
    spell_2 = models.IntegerField()
    stats = models.OneToOneField(RawStat)
    sub_type = models.CharField(max_length=24)
    team_id = models.IntegerField()
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField(auto_now=True)

    champion_key = models.CharField(max_length=32)

    objects = GameManager()

    # def __str__(self):
    #     return '%s on %s (Team %d) [GID: %d]' % (self.summoner_id.name, self.champion_id, self.team_id, self.game_id)

    def create_date_str(self):
        """Convert create_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.create_date/1000))

    def win(self):
        return self.stats.win

    class Meta:
        """These fields, taken together, ensure no duplicates are created."""
        unique_together = ('region', 'game_id', 'summoner_id')