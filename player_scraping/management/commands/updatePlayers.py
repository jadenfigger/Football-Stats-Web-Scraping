from django.core.management.base import BaseCommand
import logging
from player_scraping.api_service import APIService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Usage
        APIService.fetch_data_all(100, False)
