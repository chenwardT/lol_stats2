from django.test import TestCase

from summoners.models import Summoner
from .summoners import SingleSummoner

# FIXME: As it stands, this exceeds the rate limit and starts failing for reasons related.
# Possible fixes:
#   - emulate rate limiting
#   - mock calls to Riot's API
class SingleSummonerTestCase(TestCase):
    def setUp(self):
        self.known_summoner = Summoner.objects.create(summoner_id=1, name='Laughing Stapler',
                                                      region='NA', std_name='laughingstapler',
                                                      profile_icon_id=123)
        self.summoner_name = 'Laughing Stapler'
        self.region = 'NA'

    # Is this even necessary? If so, need to also delete everything that SingleSummoner
    # queries create, like matches, leagues, etc.
    # def tearDown(self):
    #     Summoner.objects.all().delete()

    def test_init_by_name(self):
        ss = SingleSummoner(name='Laughing Stapler', region='NA')
        self.assertEqual(ss.std_name, 'laughingstapler')
        self.assertEqual(ss.region, 'NA')

    def test_init_by_id(self):
        ss = SingleSummoner(summoner_id=123456, region='NA')
        self.assertEqual(ss.summoner_id, 123456)
        self.assertEqual(ss.region, 'NA')

    def test_is_known(self):
        ss = SingleSummoner(name=self.summoner_name, region=self.region)
        self.assertTrue(ss.is_known())

        ss = SingleSummoner(name='RiotNonextantName', region='NA')
        self.assertFalse(ss.is_known())

    def test_first_time_query_of_extant_summoner(self):
        name = 'Ronfar'
        region = 'NA'
        ss = SingleSummoner(name=name, region=region)
        self.assertFalse(ss.is_known())
        result = ss.first_time_query()

        self.assertTrue(result)
        self.assertTrue(Summoner.objects.filter(region=region).filter(name__iexact=name).exists())
        self.assertEqual(Summoner.objects.filter(region=region).filter(name__iexact=name).count(), 1)

    def test_first_time_query_of_nonextant_summoner(self):
        """
        Ensure the summoner query fails and the query is added to the InvalidSummonerQuery table.
        """
        name = 'RiotNonextantName'
        region = 'NA'
        ss = SingleSummoner(name=name, region=region)
        result = ss.first_time_query()

        self.assertFalse(result)
        self.assertFalse(Summoner.objects.filter(region=region).filter(name__iexact=name).exists())
        self.assertTrue(ss.is_invalid_query())


