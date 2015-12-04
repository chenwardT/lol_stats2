import logging
from datetime import timedelta, datetime

import pytz
from django.apps import apps
from django.db import models, transaction

from utils.functions import standardize_name

logger = logging.getLogger(__name__)


class SummonerManager(models.Manager):
    def create_summoner(self, region, attrs):
        region = region.upper()

        return self.create(summoner_id=attrs['id'],
                           name=attrs['name'],
                           std_name=standardize_name(attrs['name']),
                           profile_icon_id=attrs['profileIconId'],
                           revision_date=attrs['revisionDate'],
                           summoner_level=attrs['summonerLevel'],
                           region=region)

    def create_summoner_from_match(self, region, attrs):
        region = region.upper()

        return self.create(summoner_id=attrs['summonerId'],
                           profile_icon_id=attrs['profileIcon'],
                           name=attrs['summonerName'],
                           std_name=standardize_name(attrs['summonerName']),
                           region=region.upper())

    def create_or_update_summoner_from_match(self, region, attrs):
        # TODO: Define ttl constant elsewhere.
        summoner_ttl = timedelta(days=7)
        summoner_id = attrs['summonerId']
        region = region.upper()

        with transaction.atomic():
            if self.is_known(summoner_id, region):
                summoner = Summoner.objects.get(summoner_id=summoner_id, region=region)

                if summoner.last_update < datetime.now(tz=pytz.utc) - summoner_ttl:
                    summoner.update_from_match(attrs)
            else:
                summoner = self.create_summoner_from_match(region, attrs)

        return summoner

    def is_known(self, summoner_id, region):
        return self.filter(summoner_id=summoner_id, region=region).exists()


class Summoner(models.Model):
    """Maps to Riot API summoner DTO.

    Also contains fields for:
    -timestamp for when object was last updated.
    -standardized summoner name.
    """
    # TODO: Set to something reasonable; 20 min?
    SUMMONER_TTL = timedelta(seconds=1)
    MATCHES_TTL = timedelta(minutes=1)
    LEAGUES_TTL = timedelta(minutes=1)
    USER_REFRESH_TTL = timedelta(minutes=20)    # Cooldown between user-initiated refreshes

    summoner_id = models.BigIntegerField(db_index=True)

    # The name as it appears in game.
    # Names "should" be 16 chars, but sometimes we get weird names like
    # "IS141dca1d0484dcf8adc09". It is safe to say that any summoner object
    # that has a name of that form is not data we want to be working with;
    # they should not be referenced by any current riot-sourced data.
    name = models.CharField(max_length=24)

    # This is `name` as lowercase with spaces stripped.
    std_name = models.CharField(max_length=24, db_index=True)
    profile_icon_id = models.IntegerField()

    # Milliseconds epoch TS since something was updated about this summoner,
    # see API docs.
    # Probably not useful for us, since if this is accurate,
    # then we already queried riot API.
    revision_date = models.BigIntegerField(null=True, blank=True)
    summoner_level = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=4, db_index=True)
    last_update = models.DateTimeField(auto_now=True)
    last_matches_update = models.DateTimeField(null=True, blank=True)
    last_leagues_update = models.DateTimeField(null=True, blank=True)
    last_full_update = models.DateTimeField(null=True, blank=True)  # Used by SingleSummoner

    objects = SummonerManager()

    def update(self, region, attrs):
        """
        Update this summoner's fields completely, as would occur when directly
        querying this summoner from Riot's API.
        """
        self.summoner_id = attrs['id']
        self.name = attrs['name']
        self.std_name = standardize_name(attrs['name'])
        self.profile_icon_id = attrs['profileIconId']
        self.revision_date = attrs['revisionDate']
        self.summoner_level = attrs['summonerLevel']
        self.region = region.upper()        # Unnecessary to touch region?
        self.save()

    def update_from_match(self, attrs):
        """
        Updates this summoner's fields based on what is available from a match response.
        """
        self.profile_icon_id = attrs['profileIcon']
        self.name = attrs['summonerName']
        self.std_name = standardize_name(attrs['summonerName'])
        self.save()

    def is_complete(self):
        """
        Returns True if appropriate fields are filled in.

        Otherwise returns False, such as when the Summoner is created from match data,
        when it will be missing e.g. summoner level.
        """
        to_check = ('id',
                    'summoner_id',
                    'name',
                    'std_name',
                    'profile_icon_id',
                    'revision_date',
                    'summoner_level',
                    'region')

        return False not in map(lambda field: getattr(self, field) is not None,
                                [field for field in to_check])

    def most_recent_match_date(self):
        """
        Returns a datetime representation of this summoner's most recently played match that
        is stored, or None if no matches are stored for this summoner.
        """
        match_model = apps.get_model('matches.MatchDetail')
        match_date = match_model.objects\
            .filter(participantidentity__summoner__id=self.id)\
            .values_list('match_creation', flat=True)\
            .order_by('-match_creation')\
            .first()

        if match_date:
            return datetime.fromtimestamp(match_date/1000, tz=pytz.utc)
        else:
            return None

    def matches(self, limit=10):
        """
        Returns a QuerySet containing this summoner's matches in reverse chronological order.

        Accepts a limit on the number of matches returned. Setting `limit` to False will return all matches.
        """
        match_detail = apps.get_model('matches', 'MatchDetail')
        pi_set = self.participantidentity_set.all()

        if limit:
            return match_detail.objects.filter(participantidentity=pi_set).order_by('match_creation').reverse()[:limit]
        else:
            return match_detail.objects.filter(participantidentity=pi_set).order_by('match_creation').reverse()

    def league(self):
        """
        Returns this summoner's solo queue league.
        """
        return self.league_entry().league

    def league_entry(self):
        """
        Returns this summoner's solo queue league entry.
        """
        league_entry = apps.get_model('leagues', 'LeagueEntry')
        return league_entry.objects.filter(league__region=self.region, league__queue='RANKED_SOLO_5x5')\
            .get(player_or_team_id=self.summoner_id)

    def is_refreshable(self):
        if self.last_full_update:
            return self.last_full_update < datetime.now(tz=pytz.utc) - Summoner.USER_REFRESH_TTL
        else:
            return True

    def is_matches_refreshable(self):
        return self.last_matches_update < datetime.now(tz=pytz.utc) - Summoner.MATCHES_TTL

    def is_leagues_refreshable(self):
        return self.last_leagues_update < datetime.now(tz=pytz.utc) - Summoner.LEAGUES_TTL

    def set_last_full_update(self):
        self.last_full_update = datetime.now(tz=pytz.utc)
        self.save()

    class Meta:
        unique_together = ('summoner_id', 'region')
        index_together = ('summoner_id', 'region')
        get_latest_by = 'last_update'

    def __str__(self):
        return "[{}] {}".format(self.region, self.name)


class InvalidSummonerQueryManager(models.Manager):
    def contains(self, name, region):
        """
        Returns True if the name-region combination matches an InvalidSummonerQuery object
        that hasn't expired, otherwise False.
        """
        name = standardize_name(name)
        region = region.upper()
        query = self.filter(name=name, region=region)

        if query.exists() and not query.get().is_expired():
            return True
        else:
            return False


# TODO: Create periodic task to remove expired objects.
class InvalidSummonerQuery(models.Model):
    """
    The presence of one of these records matching a standardized search from our front end results
    in bypassing the get_summoners task and presenting the user with the summoner-not-found page.

    If a user's search for an unknown summoner results in a 404 from Riot, a matching standardized
    record is created. Records are removed after an expiry period, upon which a get_summoner request
    for the queried summoner will be executable, instead of shortcutting to the summoner-not-found
    page.
    """
    TTL = timedelta(seconds=5)

    name = models.CharField(max_length=24)
    region = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = InvalidSummonerQueryManager()

    def save(self, *args, **kwargs):
        """
        Ensure we save the name and region in the standard form.
        """
        self.name = standardize_name(self.name)
        self.region = self.region.upper()
        super(InvalidSummonerQuery, self).save(*args, **kwargs)

    def is_expired(self):
        return datetime.now(tz=pytz.utc) > self.created_at + InvalidSummonerQuery.TTL

    def __str__(self):
        return '[{}] {}'.format(self.region, self.name)

    class Meta:
        unique_together = ('name', 'region')
