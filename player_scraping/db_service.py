import logging
from .models import Player, PlayerStat, Team, League, Match
from .stats_calculator import StatCalculator
from .forms import WeekSelectForm
from .api_service import APIService
from .exception_handler import DBException, APIException
from django.db import transaction
import random

logger = logging.getLogger(__name__)


class DBService:
    @staticmethod
    def save_player_stats(player_id, week, season, data):
        # Save player stats to the database
        try:
            if data:
                player = Player.objects.get(id=player_id)

                points = StatCalculator.calculate_points(data)
                PlayerStat.objects.update_or_create(
                    player=player,
                    season=season,
                    week=week,
                    points=points,
                )

                return round(float(points), 2)
            else:
                return 0.0
            
        except Exception as err:
            raise DBException(f"Database error: {err}")

    """Will get the player points based on player_id, week, and season.
       If the playerStat does not exist then will create one.
    Returns:
        Float: points for player
    """

    @staticmethod
    def get_player_points(player, week, season):
        player_stat = PlayerStat.objects.filter(
            player=player, week=week, season=season
        ).first()
        logger.warning(f"Player: {player_stat}")
        if player_stat:
            return player_stat.points
        else:
            return DBService.fetch_and_save_player_stats(player.id, week, season)

    @staticmethod
    def fetch_and_save_player_stats(player_id, week, season):
        # Fetch player stats from the API and save them to the database
        data = APIService.fetch_player_stats(player_id, week, season)
        logger.warning(f"data: {data}")
        if data is not None:
            return DBService.save_player_stats(player_id, week, season, data)
        else:
            return 0.0

    @staticmethod
    def get_player_roster_with_points(request):
        team = Team.objects.filter(owner=request.user).first()
        for team in Team.objects.all():
            logger.warning(f"team: {team.name}")
            logger.warning(f"team: {team.roster}")
            logger.warning(f"team: {team.owner}")
        roster = team.roster.all() if team else []
        logger.warning(f"Roster: {roster}")
        current_season = League.objects.first().season
        context = {"roster_with_points": []}

        # Handle the form
        if request.method == "POST":
            form = WeekSelectForm(request.POST)
            if form.is_valid():
                current_week = int(form.cleaned_data["week"])
            else:
                current_week = League.objects.first().current_week
        else:
            form = WeekSelectForm()
            current_week = League.objects.first().current_week

        context["current_week"] = current_week
        context["form"] = form
        for player in roster:
            player_points = DBService.get_player_points(
                player, current_week, current_season
            )
            context["roster_with_points"].append((player, player_points))

        return context
    
    """
    _summary: Get a matches team's points for a week/season.
    fetches the data from the Match's, and if no
    points exist, then will calculate points and fill team rosters
    """
    @staticmethod
    def get_match_points(match):
        match.team1_points = DBService.get_team_points(match.team1, match.week, match.season)
        match.team2_points = DBService.get_team_points(match.team2, match.week, match.season)


    @staticmethod
    def get_team_points(team, week, season):
        team_points = 0.0
        for player in team.roster.all():
            player_stat = PlayerStat.objects.filter(player=player, week=week, season=season).first()
            logger.warning(player_stat)
            if not player_stat:
                pPoints = DBService.get_player_points(player, week, season)
                team_points += pPoints
            else:
                team_points += float(player_stat.points)
        return team_points

    @staticmethod
    def get_weeks_schedule(week):
        league = League.objects.first()
        matches = Match.objects.filter(
            league_id=league, week=week, season=league.season
        )
        if not matches.exists():
            DBService.create_schedule(14)
            matches = Match.objects.filter(
                league_id=league, week=week, season=league.season
            )

        context = {"games": []}

        for match in matches:
            if not match.team1_points or match.team2_points:
                DBService.get_match_points(match)
            context["games"].append(match)

        return context

    @staticmethod
    @transaction.atomic  # To ensure all database operations within the function are done in a single database transaction
    def create_schedule(weeks):
        league = League.objects.first()
        teams = list(Team.objects.filter(league=league))
        if len(teams) < 2:
            raise Exception("At least two teams are needed to create a schedule")

        for week in range(1, weeks + 1):
            random.shuffle(teams)  # Shuffling teams every week
            for i in range(len(teams) // 2):  # Each team plays one match per week
                team1 = teams[i * 2]
                team2 = teams[i * 2 + 1]
                match = Match(
                    team1=team1,
                    team2=team2,
                    league=league,
                    week=week,
                    season=league.season,
                )
                match.save()
