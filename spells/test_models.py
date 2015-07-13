from django.test import TestCase

from .models import SummonerSpell

class TestSpells(TestCase):
    def setUp(self):
        self.attrs = \
            {'description': 'Shields your champion for 115-455 (depending on champion level) for 2 seconds.',
             'id': 21,
             'key': 'SummonerBarrier',
             'name': 'Barrier',
             'summonerLevel': 4}

    def test_create(self):
        self.assertFalse(SummonerSpell.objects.all().exists())

        SummonerSpell.objects.create_spell(self.attrs)

        self.assertEqual(SummonerSpell.objects.count(), 1)

        spell = SummonerSpell.objects.get(key='SummonerBarrier')

        self.assertEqual(spell.name, 'Barrier')