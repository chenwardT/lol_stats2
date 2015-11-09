"""
Management class for spell data retrieval.
"""

import logging

from celery import chain

from riot_api.wrapper import RiotAPI
from lol_stats2.celery import riot_api, store_static_get_summoner_spell_list

logger = logging.getLogger(__name__)


class SpellManager:
    """
    Contains methods required to update spell data.

    Manually invoked on patch days.
    """
    @staticmethod
    def get_all():
        logger.debug()
        return RiotAPI.static_get_summoner_spell_list()
