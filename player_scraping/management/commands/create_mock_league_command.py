from django.core.management.base import BaseCommand
from player_scraping.models import League, Team, Player
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = "Create a mock league with 8 teams and randomly filled rosters"

    def handle(self, *args, **options):
        league_name = "Mock League"
        league = League.objects.create(
            name=league_name, number_of_teams=8, current_week=1
        )
        league.save()

        positions = ["QB", "RB", "WR"]
        num_teams = 8

        # Query all players for each position
        players_by_position = {
            pos: list(Player.objects.filter(position=pos)) for pos in positions
        }

        for i in range(num_teams):
            # Create a new user
            username = f"team_{i+1}"
            password = "password"
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Print the username and password
            print(f"User {i+1}:")
            print(f"Username: {username}")
            print(f"Password: {password}")

            # Create a new team for the user
            team_name = f"Mock Team {i+1}"
            team = Team.objects.create(name=team_name, owner=user)
            team.save()

            # Print the team name
            print(f"Team Name: {team_name}\n")

            # Assign players to the team
            for pos in positions:
                starter = random.choice(players_by_position[pos])
                team.roster.add(starter)
                players_by_position[pos].remove(starter)
                backup = random.choice(players_by_position[pos])
                team.roster.add(backup)
                players_by_position[pos].remove(backup)

        # Save the league
        league.save()
