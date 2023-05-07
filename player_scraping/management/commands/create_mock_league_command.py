from django.core.management.base import BaseCommand
from player_scraping.models import League, Team, Player
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Create a mock league with 8 teams and randomly filled rosters'

    def handle(self, *args, **options):
        # 1. Create a League object with 8 teams
        league_name = 'Mock League'
        league = League(name=league_name, number_of_teams=8, current_week=1)
        league.save()

        # 2. Create 8 Team objects with the owner field set to a user
        team_names = ['Team 1', 'Team 2', 'Team 3', 'Team 4', 'Team 5', 'Team 6', 'Team 7', 'Team 8']
        user = User.objects.first()  # Change this to the user you want to be the owner of the teams

        teams = [Team(name=name, owner=user) for name in team_names]
        Team.objects.bulk_create(teams)

        # 3. Query the Player model to get a list of players grouped by their positions
        qbs = list(Player.objects.filter(position='QB'))
        rbs = list(Player.objects.filter(position='RB'))
        wrs = list(Player.objects.filter(position='WR'))

        # 4. Randomly assign players to the teams
        for team in teams:
            random_qb = random.choice(qbs)
            random_rb = random.choice(rbs)
            random_wr = random.choice(wrs)

            backup_qb = random.choice([qb for qb in qbs if qb != random_qb])
            backup_rb = random.choice([rb for rb in rbs if rb != random_rb])
            backup_wr = random.choice([wr for wr in wrs if wr != random_wr])

            # 5. Save the teams and their rosters in the database
            team.roster.set([random_qb, random_rb, random_wr, backup_qb, backup_rb, backup_wr])
            team.save()

