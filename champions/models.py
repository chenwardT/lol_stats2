import logging

from django.db import models
from django.apps import apps

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
    """
    champion_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=32)

    objects = ChampionManager()

    def __str__(self):
        return self.name

    # TODO: Cache args and result.
    def match_count(self, version=None, region='NA'):
        """
        Returns the number of matches that this champion has participated in.

        Accepts parameters for game version and region to consider.
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

        if version:
            queryset = queryset.filter(match_detail__match_version=version)

        return queryset.count()

    # TODO: Cache args and result.
    def win_count(self, version=None, region='NA'):
        """
        Returns the number of matches that this champion has participated in and won.

        Accepts parameters for game version and region to consider.
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

        if version:
            queryset = queryset.filter(match_detail__match_version=version)

        return queryset.count()

    # TODO: Cache args and result.
    def win_rate(self, version=None, region='NA'):
        return self.win_count(version, region) / self.match_count(version, region)