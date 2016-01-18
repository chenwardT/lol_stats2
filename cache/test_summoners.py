from django.test import TestCase

from summoners.models import Summoner
from .summoners import SingleSummoner


class SingleSummonerTestCase(TestCase):
    def setUp(self):
        self.known_summoner = Summoner.objects.create(summoner_id=1, name='Laughing Stapler',
                                                      region='NA', std_name='laughingstapler',
                                                      profile_icon_id=123)
        self.summoner_name = 'Laughing Stapler'
        self.region = 'NA'

    def test_init_by_name(self):
        known_ss = SingleSummoner(name=self.summoner_name, region=self.region)

        self.assertEqual(known_ss.std_name, 'laughingstapler')
        self.assertEqual(known_ss.region, 'NA')

        # TODO: Rewrite init to not wait on RiotAPI.get_sumoners in the event
        # that the summoner is not already known.
        # Test expectations of rewrite.


