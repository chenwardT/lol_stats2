from datetime import datetime, timedelta

import pytz
from django.test import TestCase
from freezegun import freeze_time

from .models import Summoner

class SummonerTestCase(TestCase):
    def setUp(self):
        self.attrs = {'id': 299878,
                      'name': 'Ronfar',
                      'profileIconId': 580,
                      'revisionDate': 1435387768000,
                      'summonerLevel': 30}

        # Note how matches don't include revisionDate or summonerLevel.
        self.attrs_from_match = {'matchHistoryUri': '/v1/stats/player_history/NA1/205706008',
                                 'profileIcon': 780,
                                 'summonerId': 43116448,
                                 'summonerName': 'hasahaya'}

    def test_create(self):
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_summoner(region, self.attrs)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='Ronfar')

        self.assertEqual(summoner.region, 'NA')
        self.assertEqual(summoner.revision_date, 1435387768000)

    def test_create_from_match(self):
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_summoner_from_match(region, self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='hasahaya')

        self.assertEqual(summoner.region, 'NA')
        self.assertIsNone(summoner.revision_date)

    def test_create_or_update_from_match_on_new(self):
        """
        Ensure create_or_update from match data works when summoner is new.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='hasahaya')

        self.assertEqual(summoner.region, 'NA')
        self.assertIsNone(summoner.revision_date)

    def test_create_or_update_from_match_on_existing(self):
        """
        Ensure create_or_update from match data only updates fields
        when summoner already exists.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='hasahaya')
        old_name = summoner.name
        updated_attrs_from_match = self.attrs_from_match.copy()
        updated_attrs_from_match['summonerName'] = 'Another Name'

        with freeze_time(datetime.now(tz=pytz.utc) + timedelta(days=7)):
            Summoner.objects.create_or_update_summoner_from_match(region,
                                                                  updated_attrs_from_match)
        summoner.refresh_from_db()
        new_name = summoner.name

        self.assertEqual(Summoner.objects.count(), 1)
        self.assertNotEqual(old_name, new_name)

    def test_is_known(self):
        """
        Ensure is_known is True when summoner exists, False otherwise.
        """
        self.assertFalse(Summoner.objects.is_known(self.attrs_from_match['summonerId'],
                                                   'NA'))
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        self.assertTrue(Summoner.objects.is_known(self.attrs_from_match['summonerId'],
                                                  'NA'))

    def test_update_all_fields_on_summoner_that_was_complete(self):
        """
        Ensure update works on extant summoner.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_summoner(region, self.attrs)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='Ronfar')

        self.assertTrue(summoner.is_complete())

        old_name = summoner.name
        old_revision_date = summoner.revision_date

        updated_attrs = self.attrs.copy()
        updated_attrs['name'] = 'Another Name'
        updated_attrs['revisionDate'] = '1125325564000'

        summoner.update('NA', updated_attrs)
        summoner.refresh_from_db()

        new_name = summoner.name
        new_revision_date = summoner.revision_date

        self.assertEqual(Summoner.objects.count(), 1)
        self.assertNotEqual(old_name, new_name)
        self.assertNotEqual(old_revision_date, new_revision_date)

    def test_update_all_fields_on_summoner_that_was_incomplete(self):
        """
        Ensure update works on summoner that exists, but was not complete.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='hasahaya')

        self.assertFalse(summoner.is_complete())
        self.assertIsNone(summoner.revision_date)

        old_name = summoner.name
        old_revision_date = summoner.revision_date

        updated_attrs = self.attrs.copy()
        updated_attrs['summonerName'] = 'Another Name'
        updated_attrs['revisionDate'] = '1125325564000'

        summoner.update('NA', updated_attrs)
        summoner.refresh_from_db()

        new_name = summoner.name
        new_revision_date = summoner.revision_date

        self.assertEqual(Summoner.objects.count(), 1)
        self.assertNotEqual(old_name, new_name)
        self.assertIsNotNone(new_revision_date)
        self.assertNotEqual(old_revision_date, new_revision_date)

    def test_update_from_match_on_incomplete(self):
        """
        Ensure update_from_match works on incomplete summoner.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='hasahaya')

        old_name = summoner.name

        updated_attrs_from_match = self.attrs_from_match.copy()
        updated_attrs_from_match['summonerName'] = 'Another Name'

        summoner.update_from_match(updated_attrs_from_match)
        summoner.refresh_from_db()
        new_name = summoner.name

        self.assertEqual(Summoner.objects.count(), 1)
        self.assertNotEqual(old_name, new_name)

    def test_update_from_match_on_complete(self):
        """
        Ensure update_from_match works on complete summoner.
        """
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_summoner(region, self.attrs)

        self.assertEqual(Summoner.objects.count(), 1)

        summoner = Summoner.objects.get(name='Ronfar')

        old_name = summoner.name

        updated_attrs_from_match = self.attrs_from_match.copy()
        updated_attrs_from_match['summonerName'] = 'Another Name'

        summoner.update_from_match(updated_attrs_from_match)
        summoner.refresh_from_db()
        new_name = summoner.name

        self.assertEqual(Summoner.objects.count(), 1)
        self.assertNotEqual(old_name, new_name)

    def test_is_complete(self):
        self.assertFalse(Summoner.objects.all().exists())

        region = 'na'
        Summoner.objects.create_or_update_summoner_from_match(region,
                                                              self.attrs_from_match)

        self.assertEqual(Summoner.objects.count(), 1)

        incomplete_summoner = Summoner.objects.get(name='hasahaya')

        self.assertFalse(incomplete_summoner.is_complete())

        Summoner.objects.create_summoner(region, self.attrs)

        self.assertEqual(Summoner.objects.count(), 2)

        complete_summoner = Summoner.objects.get(name='Ronfar')

        self.assertTrue(complete_summoner.is_complete())