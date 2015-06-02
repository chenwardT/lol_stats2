"""
Management class for champion data retrieval.
"""

import logging
import pytz
from datetime import datetime

from champions.models import Champion
from riot_api.wrapper import RiotAPI

logger = logging.getLogger(__name__)

# TODO: Consider applications for args of these RiotWatcher methods.
class ChampionManager:
    """
    Contains methods required to get and update champion data.

    These will probably be invoked manually on patch days.
    """
    @staticmethod
    def get_all():
        logger.info('Champions - Get All')
        RiotAPI.static_get_champion_list()
