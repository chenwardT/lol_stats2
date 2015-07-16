import logging

from django.db import models

logger = logging.getLogger(__name__)

class SpellManager(models.Manager):
    def create_spell(self, attrs):
        logger.debug(attrs)

        spell = self.create(spell_id=attrs['id'],
                            summoner_level=attrs['summonerLevel'],
                            name=attrs['name'],
                            key=attrs['key'],
                            description=attrs['description'])

        return spell

class SummonerSpell(models.Model):
    """Maps to Riot API summonerSpell DTO."""
    spell_id = models.IntegerField(primary_key=True)
    summoner_level = models.IntegerField()
    name = models.CharField(max_length=16)
    key = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    objects = SpellManager()

    def __str__(self):
        return self.name
