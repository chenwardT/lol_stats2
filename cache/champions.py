"""
Management class for champion data retrieval.
"""

import logging
from datetime import datetime

import pytz

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
        logger.debug()
        RiotAPI.static_get_champion_list()
