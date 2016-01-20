import logging

from django.db import models
from django.apps import apps

from stats.models import ChampionStats
from utils.functions import is_complete_version, get_latest_version

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

    def total_picks(self, lane='ALL', role='ALL', version='ALL', region='NA'):
        """
        Returns the number of matches that this champion has participated in.

        Accepts parameters for lane, role, game version and region to consider.
        See utils.constants for valid options for lane, role and region.

        Valid options for `version` are:
            -Complete version string, e.g. '5.21.0.413'.
            -Incomplete version string, e.g. '5.21'. This will match the most significant
             version numbers. Any string containing less than 4 groups of integers will
             be considered incomplete.
            -'ALL'. This will match all versions.

        If `region` is omitted, it will default to 'NA'.

        Note that the summing logic only applies to ranked matches, where only one team
        may have any given champion.
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

    def total_wins(self, lane='ALL', role='ALL', version='ALL', region='NA'):
        """
        Returns the number of matches that this champion has participated in and won.

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

    def total_losses(self, lane='ALL', role='ALL', version='ALL', region='NA'):
        """
        Returns the number of matches that this champion has participated in and won.

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

    # TODO: Unused for now - consider moving calculations to separate module.
    def win_rate(self, lane, role, version=None, region='NA'):
        try:
            return self.total_wins(lane, role, version, region) / self.total_picks(lane, role, version, region) * 100
        except ZeroDivisionError:
            logger.exception('ZeroDivisionError: are there 0 matches?')
            return -1