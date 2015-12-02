"""
Management class for champion data retrieval.
"""

import logging

from celery import chain

from riot_api.wrapper import RiotAPI
from lol_stats2.celery import riot_api, store_champion_list

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
        chain(RiotAPI.static_get_champion_list(),
              riot_api.s(),
              store_champion_list.s())()
