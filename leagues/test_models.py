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
                      'seriesLosses': 1,
                      'seriesProgress': 'WWL',
                      'seriesTarget': 3,
                      'seriesWins': 2},
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
                      'seriesLosses': 1,
                      'seriesProgress': 'WL',
                      'seriesTarget': 2,
                      'seriesWins': 1},
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
        updated_attrs = self.attrs

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