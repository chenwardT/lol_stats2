from django.test import TestCase
from django.forms.models import model_to_dict

from .models import Champion

class ChampionTestCase(TestCase):

    def setUp(self):
        self.champ = {'id': 3000, 'key': 'Wilgo', 'name': 'Wilgo', 'title': 'the Wickerman'}
        Champion.objects.create_champion(self.champ)

    def test_champion_created(self):
        self.assertTrue(Champion.objects.filter(name='Wilgo').exists())
        wilgo = Champion.objects.get(name='Wilgo')

        wilgo_dict = model_to_dict(wilgo)

        # Model uses `champion_id` instead of `id`.
        champion_dict = self.champ
        champion_dict.pop('id')
        champion_dict['champion_id'] = 3000

        self.assertDictEqual(champion_dict, wilgo_dict)