from django.core.management.base import BaseCommand
from player_scraping.models import (
    League,
    Team,
    Player,
    Match,
)
from django.contrib.auth.models import User
import random
import logging

logger = logging.getLogger(__name__)

player_pos = ["QB", "RB", "WR"]


class Command(BaseCommand):
    help = "Create a mock league with 8 teams and randomly filled rosters"

    def handle(self, *args, **options):
        # Create a few users
        self.users = [
            User.objects.create_user(username=f"user{i}", password="password")
            for i in range(4)
        ]

        # Create a league
        self.league = League.objects.create(
            name="Test League", number_of_teams=4, current_week=1
        )

        # Create 8 teams
        self.teams = [
            Team.objects.create(name=f"Team{i}", owner=user, league=self.league)
            for i, user in enumerate(self.users)
        ]

        player_pos_ids = {
            "qb": [
                2330,
                4038941,
                12483,
                3139477,
                16757,
                3915511,
                2577417,
                3918298,
                14880,
                8439,
                11237,
                16760,
                4241464,
                3917315,
                5536,
                14876,
                4360310,
                2573079,
                2565969,
                3046779,
                4040715,
                14881,
                4360310,
                2573079,
                3046779,
                4040715,
            ],
            "rb": [
                4242335,
                3128720,
                3116385,
                4241457,
                3116593,
                4360294,
                3051392,
                4241555,
                3043078,
                3925347,
                2576434,
                3068267,
                4361579,
                3117256,
                3128390,
                3932905,
                3916566,
            ],
            "wr": [
                2977187,
                16737,
                4362628,
                4047650,
                16800,
                16460,
                2976212,
                4262921,
                15847,
                3045138,
                3046439,
                3116365,
                3116406,
                3135321,
                3930086,
                15795,
                2577327,
                2976499,
                3068267,
                3932905,
                3916566,
                4361411,
                13229,
            ],
        }

        # Fetch players by their IDs
        self.players = {}
        for pos, ids in player_pos_ids.items():
            players = Player.objects.filter(id__in=ids)
            if not players.exists():
                raise Exception(
                    f"No players found for the provided IDs in position {pos}"
                )
            self.players[pos] = list(players)

        for i, team in enumerate(self.teams):
            for pos, players in self.players.items():
                if len(players) < 2:
                    raise Exception(
                        f"Not enough players in position {pos} for team {i}"
                    )
                selected_players = random.sample(players, 2)
                for player in selected_players:
                    team.roster.add(player)
                    players.remove(player)

        # Create matches
        for week in range(1, 11):  # 10 weeks per season
            for i in range(0, 4, 2):  # 4 matches per week
                Match.objects.create(
                    team1=self.teams[i],
                    team2=self.teams[i + 1],
                    league=self.league,
                    week=week,
                    season=2022,
                    team1_points=None,
                    team2_points=None,
                )
