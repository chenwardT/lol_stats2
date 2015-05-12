import logging

from django.db import models

logger = logging.getLogger(__name__)


class SummonerManager(models.Manager):
    def create_summoner(self, region, attrs):
        logger.info("Creating summoner from: {}".format(attrs))
        summoner = self.create(summoner_id=attrs['id'],
                               name=attrs['name'],
                               std_name=attrs['name'].replace(' ', '').lower(),
                               profile_icon_id=attrs['profileIconId'],
                               revision_date=attrs['revisionDate'],
                               summoner_level=attrs['summonerLevel'],
                               region=region)
        return summoner


class Summoner(models.Model):
    """Maps to Riot API summoner DTO.

    Also contains:
    -timestamp for when object was last updated.
    -standardized summoner name.
    """
    summoner_id = models.BigIntegerField()

    # The name as it appears in game.
    # Names "should" be 16 chars, but sometimes we get weird names like
    # "IS141dca1d0484dcf8adc09". It is safe to say that any summoner object
    # that has a name of that form is not data we want to be working with;
    # they should not be referenced by any current riot-sourced data.
    name = models.CharField(max_length=24)

    # This is `name` as lowercase with spaces stripped.
    std_name = models.CharField(max_length=24)
    profile_icon_id = models.IntegerField()
    revision_date = models.BigIntegerField()    # milliseconds epoch TS
    summoner_level = models.IntegerField()      # 'long' in DTO, but we know it's <= 30
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField(auto_now=True)

    objects = SummonerManager()

    class Meta:
        unique_together = ('summoner_id', 'region')

    def __str__(self):
        return "[{}] {}".format(self.region.upper(), self.name)