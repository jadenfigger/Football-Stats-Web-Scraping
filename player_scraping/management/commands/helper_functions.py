from django.core.management.base import BaseCommand
from player_scraping.models import (
    League,
    Team,
    Player,
    Match,
)
import logging

logger = logging.getLogger(__name__)

player_pos = ["QB", "RB", "WR"]


class Command(BaseCommand):
    help = "Create a mock league with 8 teams and randomly filled rosters"

    def handle(self, *args, **options):
        # Fetch and save player points for a particular week and season.
        # player_points = PlayerDataService.get_player_points(
        #         player, current_week, current_season
        #     )

        # Fetch and save player points for entire roster for week/season

        # Fetch and save player points for entire league for week/season

        #

        pass
