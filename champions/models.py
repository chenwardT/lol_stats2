import logging

from django.db import models
from django.apps import apps
from django.db.models import Sum, Avg

from stats.models import ChampionStats
from utils.functions import is_complete_version, get_latest_version
from utils.constants import VALID_LANE_ROLE_COMBOS

logger = logging.getLogger(__name__)


class ChampionManager(models.Manager):
    # TODO: Replaceable by Champion.objects.create()
    def create_champion(self, attrs):
        """
        Create a Champion from a dict.
        """
        logger.debug(attrs)

        champion = self.create(champion_id=attrs['id'],
                               title=attrs['title'],
                               name=attrs['name'],
                               key=attrs['key'])

        return champion

class Champion(models.Model):
    """
    Maps to Riot API champion DTO.

    Contains methods to determine and store summation-related statistics.
    """
    champion_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=32)

    objects = ChampionManager()

    # TODO: This is currently a subset of all fields that make sense to sum (for later averaging).
    # It should be expanded once dynamic summing is known to work correctly.
    # See dynamic_participant_field_sum.
    #
    # Compare with stats like total_picks, where result is based on summing a
    # count of matches.
    aggregable_participant_fields = [
        'assists',
        'deaths',
        'gold_earned',
        'kills',
        'largest_killing_spree',
        'total_damage_dealt',
        'total_damage_taken',
        'total_heal',
        'minions_killed',
        'neutral_minions_killed_enemy_jungle',
        'neutral_minions_killed_team_jungle',
    ]

    def __str__(self):
        return self.name

    # TODO: Create a means of determining how to traverse related tables so we can get to
    # match_version from any starting point/model manager.
    def _mutate_participant_query_for_version(self, queryset, version):
        """
        Accepts a version string and a queryset on ParticipantManager.

        Returns a 2-tuple of the following:
            - a queryset, modified to filter by the appropriate version(s)
            - a boolean value indicating if the version string was a complete version
        """
        complete_version = is_complete_version(version)

        if version == 'LATEST':
            version = get_latest_version()

        if version and version != 'ALL':
            if complete_version:
                queryset = queryset.filter(match_detail__match_version=version)
            else:
                queryset = queryset.filter(match_detail__match_version__startswith=version)

        return (queryset, complete_version)

    def total_picks(self, lane='ALL', role='ALL', version='ALL', region='ALL'):
        """
        Returns the number of matches that this champion has participated in.

        Accepts parameters for lane, role, game version and region to consider.
        See utils.constants for valid options for lane, role and region.

        Valid options for `version` are:
            -Complete version string, e.g. '5.21.0.413'.
            -Incomplete version string, e.g. '5.21'. This will match the
             most significant version numbers.
             See utils.functions.is_complete_version.
            -'ALL'. This will match all versions.

        If `region` is omitted, it will default to 'ALL'.

        Note that the summing logic only applies to ranked matches, where only
        one team may have any given champion.
        """
        Participant = apps.get_model('matches', 'Participant')

        queryset = Participant.objects.select_related('match_detail') \
            .filter(match_detail__region=region) \
            .filter(champion_id=self.champion_id)

        if lane and lane != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        queryset, complete_version = self._mutate_participant_query_for_version(queryset, version)

        result = queryset.count()

        ChampionStats.objects.upsert(lane, role, version, complete_version, region,
                                     self.champion_id, {'sum_picks': result})

        return result

    def total_bans(self, version='ALL', region='ALL'):
        """
        Returns and stores the number of matches that this champion was
        banned in.
        """
        MatchDetail = apps.get_model('matches', 'MatchDetail')

        queryset = MatchDetail.objects.filter(region=region) \
            .filter(team__bannedchampion__champion_id=self.champion_id)

        if version == 'LATEST':
            version = get_latest_version()

        complete_version = is_complete_version(version)

        if version and version != 'ALL':
            if complete_version:
                queryset = queryset.filter(match_version=version)
            else:
                queryset = queryset.filter(match_version__startswith=version)

        result = queryset.count()

        ChampionStats.objects.upsert('ANY', 'ANY', version, complete_version, region,
                                     self.champion_id, {'sum_bans': result})

    def total_wins(self, lane='ALL', role='ALL', version='ALL', region='ALL'):
        """
        Returns and stores the number of matches that this champion has
        participated in and won.

        See total_picks method on this class for a description of parameters.
        """
        Participant = apps.get_model('matches', 'Participant')

        queryset = Participant.objects.select_related('match_detail') \
            .filter(match_detail__region=region) \
            .filter(champion_id=self.champion_id) \
            .filter(winner=True)

        if lane and lane != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        queryset, complete_version = self._mutate_participant_query_for_version(queryset, version)

        result = queryset.count()

        ChampionStats.objects.upsert(lane=lane, role=role, version=version,
                                     is_exact_version=complete_version,
                                     region=region, champion_id=self.champion_id,
                                     update_fields={'sum_wins': result})

        return result

    def total_losses(self, lane='ALL', role='ALL', version='ALL', region='ALL'):
        """
        Returns and stores the number of matches that this champion has
        participated in and won.

        See total_picks method on this class for a description of parameters.
        """
        Participant = apps.get_model('matches', 'Participant')

        queryset = Participant.objects.select_related('match_detail') \
            .filter(match_detail__region=region) \
            .filter(champion_id=self.champion_id) \
            .filter(winner=False)

        if lane and lane != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        queryset, complete_version = self._mutate_participant_query_for_version(queryset, version)

        result = queryset.count()

        ChampionStats.objects.upsert(lane=lane, role=role, version=version,
                                     is_exact_version=complete_version,
                                     region=region, champion_id=self.champion_id,
                                     update_fields={'sum_losses': result})

        return result

    # TODO: Make necessary changes to this and what follows now that `region` isn't used in filter!
    def participant_field_agg(self, field, op, lane='ALL', role='ALL', version='ALL', region='ALL'):
        """
        Dynamically aggregates the values of a given field across Participant records
        matching the provided filters using the operation specified.

        The result is stored in a matching ChampionStats Bucket and returned.

        Valid values for `op`:
            - 'sum'
            - 'avg'

        See Champion.summable_participant_fields.
        """
        logger.debug('Calculating "{}" using "{}" for {} lane={} region={} version={} region={}'.format(
            field, op, self.name, lane, role, version, region))

        if op not in ('sum', 'avg'):
            raise ValueError('Invalid aggregate op; choices are: sum, avg.')

        Participant = apps.get_model('matches', 'Participant')

        queryset = Participant.objects.select_related('match_detail') \
            .filter(champion_id=self.champion_id) \
            # .filter(match_detail__region=region)


        if lane and lane != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role != 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        queryset, complete_version = self._mutate_participant_query_for_version(queryset, version)

        if op == 'sum':
            aggregator = Sum
        elif op == 'avg':
            aggregator = Avg

        result = queryset.aggregate(aggregator(field))['{}__{}'.format(field, op.lower())]

        logger.debug('Result for {} {}_{}: {}'.format(self.name, field, op, result))

        ChampionStats.objects.upsert(lane=lane, role=role, version=version,
                                     is_exact_version=complete_version,
                                     region=region, champion_id=self.champion_id,
                                     update_fields={'{}_{}'.format(op.lower(), field): result})

        return result

    def is_significant_position(self, lane, role, version, pct=.10):
        """
        Returns True if the number of matches that this champion has been played
        in the given lane and role exceeds an optionally specified percentage
        (default: .10).

        Also requires a version.

        Intended to be used as a gate for further calculations of expensive
        statistics.
        """
        Participant = apps.get_model('matches', 'Participant')
        MatchDetail = apps.get_model('matches', 'MatchDetail')
        total_matches = MatchDetail.objects.by_version(version) \
                                           .filter(participant__champion_id=self.champion_id) \
                                           .count()
        picked_in = Participant.objects.filter(match_detail__match_version__startswith=version,
                                               champion_id=self.champion_id,
                                               participanttimeline__lane=lane,
                                               participanttimeline__role=role).count()

        return picked_in / total_matches > pct

    # TODO: Could be rewritten using partial from functools, or a closure.
    def get_significant_positions(self, version, force_update=False, pct=.10):
        """
        Returns a list of positions that this champion is commonly played in.

        See Champion.is_significant_position.
        """

        if not force_update:
            return SignificantPosition.objects.filter(champion=self, version=version, pct=pct)
        else:
            positions = []
            sigpos_objs = []

            for combo in VALID_LANE_ROLE_COMBOS:
                if self.is_significant_position(combo['lane'], combo['role'], version, pct):
                    positions.append((combo['lane'], combo['role']))
                    creation_dict = {
                        'champion_id': self.champion_id,
                        'version': version,
                        'lane': combo['lane'],
                        'role': combo['role'],
                        'pct': pct,
                    }
                    sigpos_objs.append(SignificantPosition(**creation_dict))

            # Delete all SigPos objects for this version and pct and repopulate
            # the version-pct scope with the newly calculated results.
            SignificantPosition.objects.filter(version=version, pct=pct, champion=self).delete()
            results = SignificantPosition.objects.bulk_create(sigpos_objs)

            return results

class SignificantPosition(models.Model):
    """
    Contains positive results for Champion.get_significant_positions.
    """
    champion = models.ForeignKey(Champion)
    version = models.CharField(max_length=16)
    lane = models.CharField(max_length=16)
    role = models.CharField(max_length=16)
    pct = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{:12s} (v{}) {:6s} {:11s}'.format(self.champion.name,
                                                  self.version,
                                                  self.lane,
                                                  self.role)