from django.test import TestCase

from .models import League, LeagueEntry


class LeagueTestCase(TestCase):
    def setUp(self):
        self.region = 'KR'
        self.attrs = {'queue': 'RANKED_SOLO_5x5',
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
        self.created = League.objects.create_league(self.attrs, self.region)

    def test_create(self):
        """
        Ensure League and the associated entries created in setUp are correct.
        """
        self.assertEqual(self.created, League.objects.get(name="Faker's Fighters"))

        league_entries = LeagueEntry.objects.filter(
            league__name="Faker's Fighters",
            league__region='KR',
            league__tier='DIAMOND').order_by('id')
        fakers_leagueentry_set = self.created.leagueentry_set.order_by('id')
        entries = []

        for e in fakers_leagueentry_set:
            entries.append(repr(e))

        self.assertQuerysetEqual(league_entries, entries)

    def test_update(self):
        """
        Update the created League with new entries.
        """
        updated_attrs = self.attrs.copy()
        old_names = []

        for name in self.created.leagueentry_set.order_by(
                'player_or_team_name').values('player_or_team_name'):
            old_names.append(name)

        updated_attrs['entries'][0]['playerOrTeamName'] = 'challenger3'
        updated_attrs['entries'][1]['playerOrTeamName'] = 'challenger4'
        League.objects.update_league(self.created, updated_attrs, self.region)
        new_names = []

        for name in self.created.leagueentry_set.order_by(
                'player_or_team_name').values('player_or_team_name'):
            new_names.append(name)

        self.assertNotEqual(old_names, new_names)

    def test_create_or_update_on_extant(self):
        """
        Update the created league using create_or_update.
        """
        updated_attrs = self.attrs.copy()
        old_names = []

        for name in self.created.leagueentry_set.order_by(
                'player_or_team_name').values('player_or_team_name'):
            old_names.append(name)

        updated_attrs['entries'][0]['playerOrTeamName'] = 'challenger3'
        updated_attrs['entries'][1]['playerOrTeamName'] = 'challenger4'
        League.objects.create_or_update_league(updated_attrs, self.region)
        new_names = []

        for name in self.created.leagueentry_set.order_by(
                'player_or_team_name').values('player_or_team_name'):
            new_names.append(name)

        self.assertNotEqual(old_names, new_names)

    def test_create_or_update_on_new(self):
        """
        Create a new league using create_or_update.
        """
        self.created.delete()

        self.assertFalse(League.objects.filter(name="Faker's Fighters").exists())

        League.objects.create_or_update_league(self.attrs, self.region)

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
        created = league.leagueentry_set.create_entry(attrs_full)

        self.assertTrue(created.series_losses)

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
        created = league.leagueentry_set.create_entry(self.attrs_base)

        self.assertIsNone(created.series_losses)
