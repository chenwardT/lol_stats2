from django.core.management.base import BaseCommand, CommandError

from champions.models import Champion
from utils.constants import VALID_LANE_ROLE_COMBOS

class Command(BaseCommand):
    help = 'Generate champion stats from aggregations'

    def add_arguments(self, parser):
        parser.add_argument('--patch',
                            nargs='?',
                            default='6.1',
                            help='The patch number to consider')

    def handle(self, *args, **options):
        Champion.objects.full_agg_for_all(version=options['patch'])

        self.stdout.write(self.style.MIGRATE_SUCCESS('Done!'))