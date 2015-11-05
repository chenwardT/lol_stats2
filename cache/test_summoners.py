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

    def test_init_by_name_for_known_summoner(self):
        known_ss = SingleSummoner(name=self.summoner_name, region=self.region)

        self.assertEqual(known_ss.std_name, 'laughingstapler')
        self.assertEqual(known_ss.region, 'NA')
        self.assertIsNotNone(known_ss.summoner)

        # TODO: Rewrite init to not wait on RiotAPI.get_sumoners in the event
        # that the summoner is not already known.
        # Test expectations of rewrite.

    def test_init_by_name_for_unknown_summoner(self):
        unknown_ss = SingleSummoner(name='Ronfar', region='NA')

        self.assertEqual(unknown_ss.std_name, 'ronfar')
        self.assertEqual(unknown_ss.region, 'NA')

        # TODO: Find another way to ensure summoner was stored that doesn't involve
        # checking private methods.
        self.assertIsNotNone(unknown_ss._get_instance())

    def test_init_by_name_for_nonexistent_summoner(self):
        nonexistent_ss = SingleSummoner(name='abcdefghijlmnopqrst', region='NA')

        self.assertIsNone(nonexistent_ss.summoner)

