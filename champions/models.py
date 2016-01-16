import logging

from django.db import models
from django.apps import apps

from stats.models import ChampionStats

logger = logging.getLogger(__name__)

class ChampionManager(models.Manager):
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

    def total_picks(self, lane='ALL', role='ALL', version='ALL', region='NA'):
        """
        Returns the number of matches that this champion has participated in.

        Accepts parameters for lane, role, game version and region to consider.
        Valid options for `lane` are 'TOP', 'MIDDLE', 'JUNGLE', 'BOTTOM' or 'ALL'
        to consider all lanes.
        Valid options for `role` are 'SOLO', 'NONE', 'DUO', 'DUO_CARRY', 'DUO_SUPPORT'
        or 'ALL' to consider all roles.

        If `version` is omitted, it will default to all versions.
        If `region` is omitted, it will default to 'NA'.

        Note that this logic only applies to ranked matches, where only one team
        may have any given champion.
        """
        participant_model = apps.get_model('matches', 'Participant')
        match_detail_model = apps.get_model('matches', 'MatchDetail')

        # FIXME: Hack - in prod we would want a better way of getting latest version.
        if version == 'LATEST':
            version = match_detail_model.objects.order_by('match_creation').last().match_version

        queryset = participant_model.objects.select_related('match_detail') \
            .filter(match_detail__region=region) \
            .filter(champion_id=self.champion_id)

        if lane and lane is not 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role is not 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        if version and version is not 'ALL':
            queryset = queryset.filter(match_detail__match_version=version)

        result = queryset.count()

        ChampionStats.objects.upsert(lane=lane, role=role, version=version,
                                     region=region, champion_id=self.champion_id,
                                     update_fields={'total_picks': result})

        return result

    def total_wins(self, lane='ALL', role='ALL', version='ALL', region='NA'):
        """
        Returns the number of matches that this champion has participated in and won.

        Accepts parameters for lane, role, game version and region to consider.
        If `version` is omitted, it will consider all versions.
        If `region` is omitted, it will default to 'NA'.

        Note that this logic only applies to ranked matches, where only one team
        may have any given champion.
        """
        participant_model = apps.get_model('matches', 'Participant')
        match_detail_model = apps.get_model('matches', 'MatchDetail')

        # FIXME: Hack - in prod we would want a better way of getting latest version.
        if version == 'LATEST':
            version = match_detail_model.objects.order_by('match_creation').last().match_version

        queryset = participant_model.objects.select_related('match_detail') \
            .filter(match_detail__region=region) \
            .filter(champion_id=self.champion_id) \
            .filter(winner=True)

        if lane and lane is not 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__lane=lane)

        if role and role is not 'ALL':
            queryset = queryset.prefetch_related('participanttimeline_set') \
                .filter(participanttimeline__role=role)

        if version and version is not 'ALL':
            queryset = queryset.filter(match_detail__match_version=version)

        result = queryset.count()

        ChampionStats.objects.upsert(lane=lane, role=role, version=version,
                                     region=region, champion_id=self.champion_id,
                                     update_fields={'total_wins': result})

        return result

    # TODO: Unused for now - consider moving calculations to separate module.
    def win_rate(self, lane, role, version=None, region='NA'):
        try:
            return self.total_wins(lane, role, version, region) / self.total_picks(lane, role, version, region) * 100
        except ZeroDivisionError:
            logger.exception('ZeroDivisionError: are there 0 matches?')
            return -1