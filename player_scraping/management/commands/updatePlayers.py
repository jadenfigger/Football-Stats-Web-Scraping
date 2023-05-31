from django.core.management.base import BaseCommand
import logging
import asyncio
from player_scraping.services import PlayerDataService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Usage
        asyncio.run(PlayerDataService.fetch_data_all(100))
