import logging
from datetime import timedelta

from django.db import models

# FIXME: Not writing to file, but is displayed by Celery worker.
logger = logging.getLogger(__name__)

def standardize_name(name):
        return name.replace(' ', '').lower()

class SummonerManager(models.Manager):
    def create_summoner(self, region, attrs):
        logger.info("Creating summoner with region '{}' from: {}".format(region, attrs))

        summoner = self.create(summoner_id=attrs['id'],
                               name=attrs['name'],
                               std_name=standardize_name(attrs['name']),
                               profile_icon_id=attrs['profileIconId'],
                               revision_date=attrs['revisionDate'],
                               summoner_level=attrs['summonerLevel'],
                               region=region)
        return summoner

    def is_known(self, summoner, region):
        return self.filter(region=region, std_name=standardize_name(summoner)).exists()


class Summoner(models.Model):
    """Maps to Riot API summoner DTO.

    Also contains fields for:
    -timestamp for when object was last updated.
    -standardized summoner name.
    """
    # TODO: Set to something reasonable; 20 min?
    CACHE_DURATION = timedelta(minutes=1)

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

    # Milliseconds epoch TS since something was updated about this summoner,
    # see API docs.
    # Probably not useful for us, since if this is accurate,
    # then we already queried riot API.
    revision_date = models.BigIntegerField()
    summoner_level = models.IntegerField()      # 'long' in DTO, but we know it's [0,30]
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField(auto_now=True)

    objects = SummonerManager()

    def update(self, region, attrs):
        logger.info("Updating summoner with region '{}' from: {}".format(region, attrs))

        self.summoner_id = attrs['id']
        self.name = attrs['name']
        self.std_name = standardize_name(attrs['name'])
        self.profile_icon_id = attrs['profileIconId']
        self.revision_date = attrs['revisionDate']
        self.summoner_level = attrs['summonerLevel']
        self.region = region
        self.save()

    class Meta:
        unique_together = ('summoner_id', 'region')

    def __str__(self):
        return "[{}] {}".format(self.region.upper(), self.name)