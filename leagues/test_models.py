from time import sleep

from django.test import TestCase

from .models import League, LeagueEntry


class LeagueTestCase(TestCase):
    def setUp(self):
        self.region = 'KR'
        self.league_attrs = {'queue': 'RANKED_SOLO_5x5',
                      'name': "Faker's Fighters",
                      'tier': 'DIAMOND',
                      'entries': [
                          {'division': 'I',
                           'isFreshBlood': True,
                           'isHotStreak': False,
                           'isInactive': False,
                           'isVeteran': True,
                           'leaguePoints': 99,
                           'playerOrTeamId': 456789,
                           'playerOrTeamName': 'challenger1',
                           'wins': 890,
                           'losses': 569,
                           'miniSeries':
                               {'losses': 1,
                                'progress': 'WWL',
                                'target': 3,
                                'wins': 2}},
                          {'division': 'IV',
                           'isFreshBlood': False,
                           'isHotStreak': False,
                           'isInactive': False,
                           'isVeteran': True,
                           'leaguePoints': 56,
                           'playerOrTeamId': 123456,
                           'playerOrTeamName': 'challenger2',
                           'wins': 231,
                           'losses': 72,
                           'miniSeries':
                               {'losses': 1,
                                'progress': 'WWL',
                                'target': 3,
                                'wins': 2}}
                      ]}

        self.league_attrs_different_entries = {'queue': 'RANKED_SOLO_5x5',
                 'name': "Faker's Fighters",
                 'tier': 'DIAMOND',
                 'entries': [
                     {'division': 'I',
                      'isFreshBlood': True,
                      'isHotStreak': False,
                      'isInactive': False,
                      'isVeteran': True,
                      'leaguePoints': 23,
                      'playerOrTeamId': 7777,
                      'playerOrTeamName': 'challenger3',
                      'wins': 123,
                      'losses': 321,
                      'miniSeries':
                          {'losses': 2,
                           'progress': 'WLWL',
                           'target': 3,
                           'wins': 2}},
                     {'division': 'IV',
                      'isFreshBlood': False,
                      'isHotStreak': True,
                      'isInactive': False,
                      'isVeteran': True,
                      'leaguePoints': 44,
                      'playerOrTeamId': 8888,
                      'playerOrTeamName': 'challenger4',
                      'wins': 231,
                      'losses': 72,
                      'miniSeries':
                          {'losses': 1,
                           'progress': 'WWL',
                           'target': 3,
                           'wins': 2}}
                 ]}
        self.created_league = League.objects.create_league(self.league_attrs, self.region)

    def test_create(self):
        """
        Ensure League and the associated entries created in setUp are correct.
        """
        self.assertEqual(self.created_league, League.objects.get(name="Faker's Fighters"))

        league_entries = LeagueEntry.objects.filter(
            league__name="Faker's Fighters",
            league__region='KR',
            league__tier='DIAMOND').order_by('id')
        fakers_leagueentry_set = self.created_league.leagueentry_set.order_by('id')
        entries = []

        for e in fakers_leagueentry_set:
            entries.append(repr(e))

        self.assertQuerysetEqual(league_entries, entries)

    def test_update(self):
        """
        Update the created League with new entries and ensure the resulting league
        differs in entries.
        """
        updated_attrs = self.league_attrs.copy()
        league_entries_queryset = self.created_league.leagueentry_set.order_by(
            'player_or_team_name')
        old_names = [name for name in league_entries_queryset.values('player_or_team_name')]

        updated_attrs['entries'][0]['playerOrTeamName'] = 'challenger3'
        updated_attrs['entries'][1]['playerOrTeamName'] = 'challenger4'

        sleep(1)
        League.objects.update_league(self.created_league, self.league_attrs_different_entries)

        new_names = [name for name in league_entries_queryset.values('player_or_team_name')]

        self.assertNotEqual(old_names, new_names)

    def test_create_or_update_on_extant(self):
        """
        Update the created league using create_or_update and ensure the resulting league
        differs in entries.
        """
        updated_attrs = self.league_attrs.copy()
        league_entries_queryset = self.created_league.leagueentry_set.order_by(
            'player_or_team_name')
        old_names = [name for name in league_entries_queryset.values('player_or_team_name')]

        updated_attrs['entries'][0]['playerOrTeamName'] = 'challenger3'
        updated_attrs['entries'][1]['playerOrTeamName'] = 'challenger4'

        sleep(1)
        League.objects.create_or_update_league(self.league_attrs_different_entries, self.region)

        new_names = [name for name in league_entries_queryset.values('player_or_team_name')]

        self.assertNotEqual(old_names, new_names)

    def test_create_or_update_on_new(self):
        """
        Create a new league using create_or_update.
        """
        self.created_league.delete()

        self.assertFalse(League.objects.filter(name="Faker's Fighters").exists())

        League.objects.create_or_update_league(self.league_attrs_different_entries, self.region)

        self.assertTrue(League.objects.filter(name="Faker's Fighters").exists())

class LeagueEntryTestCase(TestCase):
    def setUp(self):
        self.attrs_base = {'division': 'I',
                           'isFreshBlood': True,
                           'isHotStreak': False,
                           'isInactive': False,
                           'isVeteran': True,
                           'leaguePoints': 99,
                           'playerOrTeamId': 456789,
                           'playerOrTeamName': 'challenger1',
                           'wins': 890,
                           'losses': 569}
        self.attrs_miniseries = {'miniSeries':
                                     {'losses': 1,
                                      'progress': 'WWL',
                                      'target': 3,
                                      'wins': 2}}

    def test_create_with_miniseries(self):
        """
        Create a LeagueEntry from a dict that includes miniseries data.

        Since create_league does not create an association through league_id,
        and the league_id FK requirement, we use a league's leagueentry_set.
        """
        league = League.objects.create(region='TEST',
                                       queue='TEST_QUEUE',
                                       name='TEST_NAME',
                                       tier='TEST_TIER')
        attrs_full = self.attrs_base.copy()
        attrs_full.update(self.attrs_miniseries)
        dict_of_attrs = {'entries': [attrs_full]}
        league.leagueentry_set.create_entries(dict_of_attrs)
        created = LeagueEntry.objects.order_by('id').last()

        self.assertEqual(created.series_progress, 'WWL')

    def test_create_without_miniseries(self):
        """
        Create a LeagueEntry from a dict that doesn't include miniseries data.

        Since create_league does not create an association through league_id,
        and the league_id FK requirement, we use a league's leagueentry_set.
        """
        league = League.objects.create(region='TEST',
                                       queue='TEST_QUEUE',
                                       name='TEST_NAME',
                                       tier='TEST_TIER')
        dict_of_attrs = {'entries': [self.attrs_base]}
        league.leagueentry_set.create_entries(dict_of_attrs)
        created = LeagueEntry.objects.order_by('id').last()

        self.assertEqual(created.player_or_team_id, '456789')
        self.assertIsNone(created.series_progress)
