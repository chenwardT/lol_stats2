from django.test import TestCase
from django.forms.models import model_to_dict

from .models import Champion

class ChampionTestCase(TestCase):
    def setUp(self):
        self.init_dict = {'id': 3000, 'key': 'Wilgo', 'name': 'Wilgo', 'title': 'the Wickerman'}
        self.wilgo = Champion.objects.create_champion(self.init_dict)

    def test_champion_created(self):
        """
        Create a Champion instance with create_champion, passing an init dict
        as RiotWatcher would get and ensure it has the expected attributes.
        """

        wilgo_query = Champion.objects.filter(name='Wilgo')

        self.assertEqual(self.wilgo, wilgo_query.get())

        # Compare attrs.

        wilgo_dict = model_to_dict(self.wilgo)

        # Model uses `champion_id` instead of `id`.
        self.init_dict.pop('id')
        self.init_dict['champion_id'] = 3000

        self.assertDictEqual(self.init_dict, wilgo_dict)

    def test_champion_str(self):
        """
        Ensure Champion has the correct string representation.
        """
        wilgo = Champion.objects.get(name='Wilgo')

        self.assertEqual('Wilgo', str(wilgo))
