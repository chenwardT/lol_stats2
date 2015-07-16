"""
Management class for spell data retrieval.
"""

import logging

from riot_api.wrapper import RiotAPI

logger = logging.getLogger(__name__)

class SpellManager:
    """
    Contains methods required to update spell data.

    Manually invoked on patch days.
    """
    @staticmethod
    def get_all():
        logger.debug()
        RiotAPI.static_get_summoner_spell_list()