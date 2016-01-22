from django.core.management.base import BaseCommand, CommandError

from champions.models import Champion
from utils.constants import VALID_LANE_ROLE_COMBOS
from stats.models import ChampionStats

class Command(BaseCommand):
    help = 'Generate champion stats from aggregations'

    def add_arguments(self, parser):
        parser.add_argument('op', nargs='?', type=str, default='avg')
        parser.add_argument('--region',
                            nargs='?',
                            default='NA',
                            help='The region to consider')
        parser.add_argument('--patch',
                            nargs='?',
                            default='ALL',
                            help='The patch number to consider')

    def handle(self, *args, **options):
        if options['op'] not in ('sum', 'avg'):
            raise CommandError('Invalid operation. Must be one of: sum, avg')

        for champion in Champion.objects.all():
            for combo in VALID_LANE_ROLE_COMBOS:
                # TODO: Replace the 300. Percentage-based threshold?
                queryset = ChampionStats.objects.filter(bucket__version=options['matchversion'],
                                                        bucket__region=options['region'],
                                                        bucket__lane=combo['lane'],
                                                        bucket__role=combo['role'],
                                                        champion_id=champion.champion_id)
                if queryset.exists() and queryset.get().sum_picks > 300:
                    for field in Champion.aggregable_participant_fields:
                        champion.participant_field_agg(field,
                                                       options['op'],
                                                       combo['lane'],
                                                       combo['role'],
                                                       options['patch'],
                                                       options['region'])

        rows = Champion.objects.count() * \
               len(VALID_LANE_ROLE_COMBOS) * \
               len(Champion.aggregable_participant_fields)

        self.stdout.write(self.style.MIGRATE_SUCCESS('Generated %s result(s)' % rows))