from django.db import models


class Version(models.Model):
    # TODO: Manage least-significant version field, i.e. ability to merge 5.2.0.22, 5.2.0.46, etc
    number = models.CharField(max_length=16)     # ex. '5.22.0.345', 'ALL'
    created_at = models.DateTimeField(auto_now_add=True)


class ChampionStats(models.Model):
    version = models.ForeignKey(Version)
    champion_id = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    pick_count = models.BigIntegerField()
    ban_count = models.BigIntegerField()
    win_count = models.BigIntegerField()
    loss_count = models.BigIntegerField()   # Useful for checking integrity?
