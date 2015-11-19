import logging

from django.db import models

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