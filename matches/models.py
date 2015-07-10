"""
Matches differ from Games in that they use the match/matchhistory API
which includes timelines, runes, masteries, draft phase data, events,
and associated positional data.

Fields related to game types other than SR are not included.

One-to-one fields are on child models, unless that model is referred
to by more than one kind of other model (e.g. Position).
"""

import logging
from datetime import datetime

from django.db import models, transaction
from django.contrib.postgres import fields

from utils.mixins import (IterableDataFieldsMixin,
                          CreateableFromAttrsMixin,
                          ParticipantFromAttrsMixin)
from champions.models import Champion
from summoners.models import Summoner

logger = logging.getLogger(__name__)

# TODO: Finish create_ methods for models related to timeline data.
# See `include_timeline` arg of RiotWatcher.get_match().

class MatchDetailManager(CreateableFromAttrsMixin, models.Manager):
    def create_match(self, attrs):
        match = None

        with transaction.atomic():
            if not self.filter(match_id=attrs['matchId'],
                               region=attrs['region']).exists():

                match = self.create(**self.init_dict(attrs))

        if match:
            for p in attrs['participants']:
                match.participant_set.create_participant(p)

            for pi in attrs['participantIdentities']:
                match.participantidentity_set.create_participant_identity(pi)

            for t in attrs['teams']:
                match.team_set.create_team(t)

        logging.info('Created match: {} {}'.format(attrs['region'],
                                                   attrs['matchId']))
        return match

class MatchDetail(IterableDataFieldsMixin, models.Model):
    map_id = models.IntegerField()                      # ex. 11
    match_creation = models.BigIntegerField()           # ex. 1432585774909
    match_duration = models.BigIntegerField()           # ex. 1854
    match_id = models.BigIntegerField(db_index=True)    # ex. 1835139131
    match_mode = models.CharField(max_length=16)        # ex. CLASSIC
    match_type = models.CharField(max_length=16)        # ex. MATCHED_GAME
    match_version = models.CharField(max_length=16)     # ex. 5.9.0.318
    platform_id = models.CharField(max_length=8)        # ex. NA1
    queue_type = models.CharField(max_length=24)        # ex. RANKED_SOLO_5x5
    region = models.CharField(max_length=4, db_index=True)  # ex. NA
    season = models.CharField(max_length=24)            # ex. PRESEASON2015

    objects = MatchDetailManager()

    def __str__(self):
        return '[{}] {}'.format(self.region, self.match_id)

    def match_date(self):
        return datetime.fromtimestamp(self.match_creation/1000)

    class Meta:
        unique_together = ('match_id', 'region')

class ParticipantManager(ParticipantFromAttrsMixin, models.Manager):
    def create_participant(self, attrs):
        participant = self.create(**self.init_dict(attrs))

        if 'masteries' in attrs:
            for m in attrs['masteries']:
                participant.mastery_set.create_mastery(m)

        if 'runes' in attrs:
            for r in attrs['runes']:
                participant.rune_set.create_rune(r)

        participant.participanttimeline_set.create_participant_timeline(attrs['timeline'])

        return participant

class Participant(IterableDataFieldsMixin, models.Model):
    champion_id = models.IntegerField()
    highest_achieved_season_tier = models.CharField(max_length=16, null=True, blank=True)
    participant_id = models.IntegerField()
    spell1_id = models.IntegerField()
    spell2_id = models.IntegerField()
    team_id = models.IntegerField()

    # Originally in ParticipantStats.
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

    match_detail = models.ForeignKey(MatchDetail)

    objects = ParticipantManager()

    def __str__(self):
        return '{} on team {}'.format(Champion.objects.get(champion_id=self.champion_id),
                                      self.team_id)

class ParticipantIdentityManager(CreateableFromAttrsMixin, models.Manager):
    def create_participant_identity(self, attrs):
        participant_identity = self.create(**self.init_dict(attrs))

        participant_identity.summoner = \
            Summoner.objects.create_or_update_summoner_from_match(
                participant_identity.match_detail.region, attrs['player'])

        participant_identity.save()

        return participant_identity

class ParticipantIdentity(IterableDataFieldsMixin, models.Model):
    participant_id = models.IntegerField()

    summoner = models.ForeignKey(Summoner, blank=True, null=True)
    match_detail = models.ForeignKey(MatchDetail)

    objects = ParticipantIdentityManager()

    def __str__(self):
        return 'Participant ID {} in {}'.format(self.participant_id, self.match_detail)

class TeamManager(CreateableFromAttrsMixin, models.Manager):
    def create_team(self, attrs):
        team = self.create(**self.init_dict(attrs))

        if 'bans' in attrs:
            for b in attrs['bans']:
                team.bannedchampion_set.create_banned_champion(b)

        return team

class Team(IterableDataFieldsMixin, models.Model):
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

    objects = TeamManager()

    def __str__(self):
        return '{} team of match {}'.format(self.color(), self.match_detail)

    def color(self):
        if self.team_id == 100:
            return 'Blue'
        else:
            return 'Purple'

# timeline data
class Timeline(IterableDataFieldsMixin, models.Model):
    frame_interval = models.BigIntegerField()
    # frames list

    match_detail = models.OneToOneField(MatchDetail)

class MasteryManager(CreateableFromAttrsMixin, models.Manager):
    def create_mastery(self, attrs):
        mastery = self.create(**self.init_dict(attrs))

        return mastery

class Mastery(IterableDataFieldsMixin, models.Model):
    mastery_id = models.BigIntegerField()
    rank = models.BigIntegerField()

    participant = models.ForeignKey(Participant)

    objects = MasteryManager()

# TODO: Check above all previous fields for BigInt -> Int.

class ParticipantTimelineManager(CreateableFromAttrsMixin, models.Manager):
    def create_participant_timeline(self, attrs):
        participant_timeline = self.create(**self.init_dict(attrs))

        return participant_timeline

class ParticipantTimeline(IterableDataFieldsMixin, models.Model):
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

    participant = models.ForeignKey(Participant)

    objects = ParticipantTimelineManager()

class RuneManager(CreateableFromAttrsMixin, models.Manager):
    def create_rune(self, attrs):
        rune = self.create(**self.init_dict(attrs))

        return rune

class Rune(IterableDataFieldsMixin, models.Model):
    rank = models.IntegerField()
    rune_id = models.IntegerField()

    participant = models.ForeignKey(Participant)

    objects = RuneManager()

    def __str__(self):
        return "Rune of {}: {} ({})".format(self.participant, self.rune_id, self.rank)

class BannedChampionManager(CreateableFromAttrsMixin, models.Manager):
    def create_banned_champion(self, attrs):
        banned_champion = self.create(**self.init_dict(attrs))

        return banned_champion

class BannedChampion(IterableDataFieldsMixin, models.Model):
    champion_id = models.IntegerField()
    pick_turn = models.IntegerField()

    team = models.ForeignKey(Team)

    objects = BannedChampionManager()

    def __str__(self):
        return "{} team's ban {}: {}".format(self.team.color(), self.pick_turn, self.champion_id)

# timeline data
class Frame(IterableDataFieldsMixin, models.Model):
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

# timeline data
class Event(IterableDataFieldsMixin, models.Model):
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

# timeline data
class ParticipantFrame(IterableDataFieldsMixin, models.Model):
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

# timeline data
class Position(IterableDataFieldsMixin, models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
