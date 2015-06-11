"""
Matches differ from Games in that they use the match/matchhistory API
which includes timelines, runes, masteries, draft phase data, events,
and associated positional data.

Fields related to game types other than SR are not included.

One-to-one fields are on child models, unless that model is referred
to by more than one kind of other model (e.g. Position).
"""

from django.db import models
from django.contrib.postgres import fields

from utils.functions import underscore_dict
from utils.mixins import IterableNonAutoFieldsMixin

# TODO: Create a means of creating/updating a model instance from dict
# that automatically sets instance fields to None if their associated
# key isn't present in the dict. Must be able to ignore AutoFields (like id),
# and call related model's creation methods.

class MatchDetailManager(models.Manager):
    def create_match(self, attrs):
        # match = self.create(map_id=attrs['mapId'],
        #                     match_creation=attrs['matchCreation'],
        #                     match_duration=attrs['matchDuration'],
        #                     match_id=attrs['matchId'],
        #                     match_mode=attrs['matchMode'],
        #                     match_type=attrs['matchType'],
        #                     match_version=attrs['matchVersion'],
        #                     platform_id=attrs['platformId'],
        #                     queue_type=attrs['queueType'],
        #                     region=attrs['region'],
        #                     season=attrs['season'])

        # TODO: Extract this method into mixin we can include in
        # other models.
        model_fields = [f for f in self.model.non_autofields()]
        underscore_attrs = underscore_dict(attrs)
        init_dict = {}

        # Create an initialization dict that contains just the key-value
        # pairs that are relevant to this model.
        for k in model_fields:
            init_dict[k] = underscore_attrs[k]

        match = self.create(**init_dict)


class MatchDetail(IterableNonAutoFieldsMixin, models.Model):
    map_id = models.IntegerField()                      # ex. 11
    match_creation = models.BigIntegerField()           # ex. 1432585774909
    match_duration = models.BigIntegerField()           # ex. 1854
    match_id = models.BigIntegerField()                 # ex. 1835139131
    match_mode = models.CharField(max_length=16)        # ex. CLASSIC
    match_type = models.CharField(max_length=16)        # ex. MATCHED_GAME
    match_version = models.CharField(max_length=16)     # ex. 5.9.0.318
    platform_id = models.CharField(max_length=8)        # ex. NA1
    queue_type = models.CharField(max_length=24)        # ex. RANKED_PREMADE_5x5
    region = models.CharField(max_length=4)             # ex. NA
    season = models.CharField(max_length=24)            # ex. PRESEASON2015

    objects = MatchDetailManager()

class ParticipantManager(models.Manager):
    def create_participant(self, attrs):
        # participant = self.create(champion_id=attrs['championId'],
        #                           highest_achieved_season_tier=attrs[''])

        # for f in self.model.non_autofields():
        #     print(f)
        pass


class Participant(IterableNonAutoFieldsMixin, models.Model):
    champion_id = models.IntegerField()
    highest_achieved_season_tier = models.CharField(max_length=16, null=True, blank=True)
    participant_id = models.IntegerField()
    spell1_id = models.IntegerField()
    spell2_id = models.IntegerField()
    team_id = models.IntegerField()

    match_detail = models.ForeignKey(MatchDetail)

    objects = ParticipantManager()

class ParticipantIdentity(models.Model):
    participant_id = models.IntegerField()

    match_detail = models.ForeignKey(MatchDetail)

class Team(models.Model):
    baron_kills = models.IntegerField(null=True, blank=True)
    #dominion_victory_score
    dragon_kills = models.IntegerField(null=True, blank=True)
    first_baron = models.BooleanField()
    first_blood = models.BooleanField()
    first_dragon = models.BooleanField()
    first_inhibitor = models.BooleanField()
    first_tower = models.BooleanField()
    inhibitor_kills = models.IntegerField(null=True, blank=True)
    team_id = models.IntegerField()
    tower_kills = models.IntegerField(null=True, blank=True)
    # vilemaw_kills
    winner = models.BooleanField()

    match_detail = models.ForeignKey(MatchDetail)

class Timeline(models.Model):
    frame_interval = models.BigIntegerField()
    # frames list

    match_detail = models.OneToOneField(MatchDetail)

class Mastery(models.Model):
    mastery_id = models.BigIntegerField()
    rank = models.BigIntegerField()

    participant = models.ForeignKey(Participant)

# TODO: Check above all previous fields for BigInt -> Int.

class ParticipantStats(models.Model):
    assists = models.IntegerField(null=True, blank=True)
    champ_level = models.IntegerField()
    #combat_player_score
    deaths = models.IntegerField(null=True, blank=True)
    double_kills = models.IntegerField(null=True, blank=True)
    first_blood_assist = models.BooleanField()
    first_blood_kill = models.BooleanField()
    first_inhibitor_assist = models.BooleanField()
    first_inhibitor_kill = models.BooleanField()
    first_tower_assist = models.BooleanField()
    first_tower_kill = models.BooleanField()
    gold_earned = models.IntegerField(null=True, blank=True)
    gold_spent = models.IntegerField(null=True, blank=True)
    inhibitor_kills = models.IntegerField(null=True, blank=True)
    item0 = models.IntegerField(null=True, blank=True)
    item1 = models.IntegerField(null=True, blank=True)
    item2 = models.IntegerField(null=True, blank=True)
    item3 = models.IntegerField(null=True, blank=True)
    item4 = models.IntegerField(null=True, blank=True)
    item5 = models.IntegerField(null=True, blank=True)
    item6 = models.IntegerField(null=True, blank=True)
    killing_sprees = models.IntegerField(null=True, blank=True)
    kills = models.IntegerField(null=True, blank=True)
    largest_critical_strike = models.IntegerField(null=True, blank=True)
    largest_killing_spree = models.IntegerField(null=True, blank=True)
    largest_multi_kill = models.IntegerField(null=True, blank=True)
    magic_damage_dealt = models.IntegerField(null=True, blank=True)
    magic_damage_dealt_to_champions = models.IntegerField(null=True, blank=True)
    magic_damage_taken = models.IntegerField(null=True, blank=True)
    minions_killed = models.IntegerField(null=True, blank=True)
    neutral_minions_killed = models.IntegerField(null=True, blank=True)
    neutral_minions_killed_enemy_jungle = models.IntegerField(null=True, blank=True)
    neutral_minions_killed_team_jungle = models.IntegerField(null=True, blank=True)
    # node_capture = models.IntegerField()
    # node_capture_assist = models.IntegerField()
    # node_neutralize = models.IntegerField()
    # node_neutralize_assist = models.IntegerField()
    # objective_player_score = models.IntegerField()
    penta_kills = models.IntegerField(null=True, blank=True)
    physical_damage_dealt = models.IntegerField(null=True, blank=True)
    physical_damage_dealt_to_champions = models.IntegerField(null=True, blank=True)
    physical_damage_taken = models.IntegerField(null=True, blank=True)
    quadra_kills = models.IntegerField(null=True, blank=True)
    sight_wards_bought_in_game = models.IntegerField(null=True, blank=True)
    # team_objective = models.IntegerField()
    total_damage_dealt = models.IntegerField(null=True, blank=True)
    total_damage_dealt_to_champions = models.IntegerField(null=True, blank=True)
    total_damage_taken = models.IntegerField(null=True, blank=True)
    total_heal = models.IntegerField(null=True, blank=True)
    # total_player_score = models.IntegerField()
    # total_score_rank = models.IntegerField()
    total_time_crowd_control_dealt = models.IntegerField(null=True, blank=True)
    total_units_healed = models.IntegerField(null=True, blank=True)
    tower_kills = models.IntegerField(null=True, blank=True)
    triple_kills = models.IntegerField(null=True, blank=True)
    true_damage_dealt = models.IntegerField(null=True, blank=True)
    true_damage_dealt_to_champions = models.IntegerField(null=True, blank=True)
    true_damage_taken = models.IntegerField(null=True, blank=True)
    unreal_kills = models.IntegerField(null=True, blank=True)
    vision_wards_bought_in_game = models.IntegerField(null=True, blank=True)
    wards_killed = models.IntegerField(null=True, blank=True)
    wards_placed = models.IntegerField(null=True, blank=True)
    winner = models.BooleanField()

    participant = models.OneToOneField(Participant)

class ParticipantTimeline(models.Model):
    # ParticipantTimelineData types to be added later.
    # ancient_golem_assists_per_min_counts
    # ancient_golem_kills_per_min_counts
    # assisted_lane_deaths_per_min_deltas
    # assisted_lane_kills_per_min_deltas
    # baron_assists_per_min_counts
    # baron_kills_per_min_counts
    # creeps_per_min_deltas
    # cs_diff_per_min_deltas
    # damage_taken_diff_per_min_deltas
    # damage_taken_per_min_deltas
    # dragon_assists_per_min_counts
    # dragon_kills_per_min_counts
    # elder_lizard_assists_per_min_counts
    # elder_lizard_kills_per_min_counts
    # gold_per_min_deltas
    # inhibitor_assists_per_min_counts
    # inhibitor_kills_per_min_counts
    lane = models.CharField(max_length=8)
    role = models.CharField(max_length=16)
    # tower_assists_per_min_counts
    # tower_kills_per_min_counts
    # tower_kills_per_min_deltas
    # vilemaw_assists_per_min_counts
    # vilemaw_kills_per_min_counts
    # wards_per_min_deltas
    # xp_diff_per_min_deltas
    # xp_per_min_deltas

    participant = models.OneToOneField(Participant)

class Rune(models.Model):
    rank = models.IntegerField()
    rune_id = models.IntegerField()

    participant = models.ForeignKey(Participant)

class Player(models.Model):
    match_history_uri = models.CharField(max_length=64)
    profile_icon = models.IntegerField()
    summoner_id = models.IntegerField()
    summoner_name = models.CharField(max_length=24)

    participant_identity = models.OneToOneField(ParticipantIdentity)

class BannedChampion(models.Model):
    champion_id = models.IntegerField()
    pick_turn = models.IntegerField()

    team = models.ForeignKey(Team)

class Frame(models.Model):
    #events
    #participant_frames
    timestamp = models.BigIntegerField()        # ms into the game the frame occurred

    timeline = models.ForeignKey(Timeline)

# All ParticipantTimeline fields that refer to this model are disabled.
# class ParticipantTimelineData(models.Model):
#     ten_to_twenty = models.FloatField(null=True, blank=True)
#     thirty_to_end = models.FloatField(null=True, blank=True)
#     twenty_to_thirty = models.FloatField(null=True, blank=True)
#     zero_to_ten = models.FloatField(null=True, blank=True)

class Event(models.Model):
    # ascended_type
    assisting_participant_ids = fields.ArrayField(models.IntegerField())
    building_type = models.CharField(max_length=24)         # ex. INHIBITOR_BUILDING
    creator_id = models.IntegerField()
    event_type = models.CharField(max_length=24)            # ex. ELITE_MONSTER_KILL
    item_after = models.IntegerField()
    item_before = models.IntegerField()
    item_id = models.IntegerField()
    killer_id = models.IntegerField()
    lane_type = models.CharField(max_length=16)             # ex. MID_LANE
    level_up_type = models.CharField(max_length=8)          # ex. NORMAL
    monster_type = models.CharField(max_length=16)          # ex. BARON_NASHOR
    participant_id = models.IntegerField()
    # point_captured
    position = models.OneToOneField('Position')
    skill_slot = models.IntegerField()
    team_id = models.IntegerField()
    timestamp = models.BigIntegerField()
    tower_type = models.CharField(max_length=24)            # ex. FOUNTAIN_TURRET
    victim_id = models.IntegerField()
    ward_type = models.CharField(max_length=32)             # ex. YELLOW_TRINKET_UPGRADE

    frame = models.ForeignKey(Frame)

class ParticipantFrame(models.Model):
    current_gold = models.IntegerField()
    # dominion_score = models.IntegerField()
    jungle_minions_killed = models.IntegerField()
    level = models.IntegerField()
    minions_killed = models.IntegerField()
    participant_id = models.IntegerField()
    position = models.OneToOneField('Position')
    team_score = models.IntegerField()
    total_gold = models.IntegerField()
    xp = models.IntegerField()

class Position(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
