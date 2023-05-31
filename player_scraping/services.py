import asyncio
import aiohttp
import logging
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from django.db import models
from asgiref.sync import async_to_sync, sync_to_async
from .models import Player, PlayerStat, Team, League
from .utils import get_value_at_index
from .forms import WeekSelectForm

logger = logging.getLogger(__name__)


class PlayerDataService:
    BASE_API_URL = (
        "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/"
    )

    @classmethod
    async def fetch_player_stats(cls, player_id, week, season):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?season={season}"
                ) as response:
                    if response.status != 200:
                        logger.warning(
                            f"{player_id} does not exist for the season year: {season}"
                        )
                        return None

                    data = await response.json()

                    if data.get("categories") is None:
                        logger.warning(
                            f"{player_id} does not exist for the season year: {season}"
                        )
                        return None

                    for season_type in data["seasonTypes"]:
                        if season_type["displayName"] == f"{season} Regular Season":
                            for category in season_type["categories"]:
                                if category["type"] == "event":
                                    for game in category["events"]:
                                        if (
                                            data["events"][game["eventId"]]["week"]
                                            == week
                                        ):
                                            return PlayerPointsService.extract_stats(
                                                data["names"], game["stats"]
                                            )

                    logger.warning(f"{player_id} does not exist for the week: {week}")
                    return None

            except Exception as err:
                logger.error(f"Something went wrong: {err}")

    @staticmethod
    def save_player_stats(player_id, week, season, data):
        # Save player stats to the database
        if data:
            player = async_to_sync(Player.objects.get)(id=player_id)

            points = PlayerPointsService.calculate_points(data)
            async_to_sync(PlayerStat.objects.update_or_create)(
                player=player,
                season=season,
                week=week,
                points=points,
            )

        return round(float(points), 2)

    @classmethod
    async def fetch_player_details(cls, player_id):
        async with aiohttp.ClientSession() as session:
            url = f"{cls.BASE_API_URL}{player_id}"
            async with session.get(url) as response:
                # Replace raise_for_status with your own error handling
                if response.status != 200:
                    logger.error(f"HTTP Error: {response.status}, {response.reason}")
                    return None

                player_json_data = await response.json()
                return player_json_data

    @classmethod
    async def fetch_data_limit(cls, limit, page, update_existing=False):
        async with aiohttp.ClientSession() as session:
            url = f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit={limit}&page={page}"
            async with session.get(url) as response:
                # Replace raise_for_status with your own error handling
                if response.status != 200:
                    logger.error(f"HTTP Error: {response.status}, {response.reason}")
                    return None

                json_data = await response.json()
                player_ids = [
                    player["id"] for player in json_data["items"] if player["active"]
                ]

                to_update = set(player_ids)
                if update_existing:
                    existing_players = set(
                        async_to_sync(Player.objects.filter)(
                            id__in=player_ids
                        ).values_list("id", flat=True)
                    )
                    to_update.intersection_update(existing_players)

                with ThreadPoolExecutor(max_workers=20) as executor:
                    new_player_details = list(
                        executor.map(PlayerDataService.fetch_player_details, to_update)
                    )

                players_to_create = []
                for player_detail in new_player_details:
                    if player_detail is not None:
                        player_id = player_detail["athlete"]["id"]
                        if player_id:
                            player_name = player_detail["athlete"]["fullName"]
                            full_team = (
                                player_detail["athlete"]["team"]["location"]
                                + " "
                                + player_detail["athlete"]["team"]["nickname"]
                            )
                            abr_team = player_detail["athlete"]["team"]["abbreviation"]
                            player_position = player_detail["athlete"]["position"][
                                "abbreviation"
                            ]

                            if player_position in ["QB", "RB", "WR"]:
                                players_to_create.append(
                                    Player(
                                        id=player_id,
                                        name=player_name,
                                        position=player_position,
                                        full_team=full_team,
                                        abr_team=abr_team,
                                    )
                                )

                async_to_sync(Player.objects.bulk_create)(
                    players_to_create, ignore_conflicts=True
                )

                return json_data["count"]

    @classmethod
    async def fetch_data_all(cls, limit, update_existing=True, add_and_update=False):
        count = await cls.fetch_data_limit(limit, 1, update_existing)
        total_pages = ceil(count / limit)

        tasks = [
            cls.fetch_data_limit(limit, page, update_existing)
            for page in range(2, total_pages + 1)
        ]

        await asyncio.gather(*tasks)

    @staticmethod
    def get_player_roster_with_points(request):
        team = async_to_sync(Team.objects.filter)(owner=request.user).first()
        roster = team.roster.all() if team else []
        current_season = 2022  # Assuming season is an integer

        # Handle the form
        if request.method == "POST":
            form = WeekSelectForm(request.POST)
            if form.is_valid():
                current_week = int(form.cleaned_data["week"])
            else:
                current_week = async_to_sync(League.objects.first)().current_week
        else:
            form = WeekSelectForm()
            current_week = async_to_sync(League.objects.first)().current_week

        roster_with_points = []
        for player in roster:
            player_points = PlayerDataService.get_player_points(
                player, current_week, current_season
            )
            roster_with_points.append((player, player_points))

    @staticmethod
    def fetch_and_save_player_stats(player_id, week, season):
        # Fetch player stats from the API and save them to the database
        data = async_to_sync(PlayerDataService.fetch_player_stats)(
            player_id, week, season
        )
        if data is not None:
            return async_to_sync(PlayerDataService.save_player_stats)(
                player_id, week, season, data
            )

    # Will get the player points based on player_id, week, and season. If the playerStat does not exist then will create one.
    @staticmethod
    def get_player_points(player, week, season):
        player_stat = async_to_sync(PlayerStat.objects.filter)(
            player=player, week=week, season=season
        ).first()
        if player_stat:
            return player_stat.points
        else:
            return PlayerDataService.fetch_and_save_player_stats(
                player.id, week, season
            )


class PlayerPointsService:
    @staticmethod
    def calculate_points(stats):
        # You can modify this formula based on your league's point system
        # stats = [pass_yds, rush_atms, rush_yds, tot_rec, rec_yds, touchdowns]
        logger.warning(stats)
        points = (
            stats[0] * 0.05
            + stats[1] * 0.1
            + stats[2] * 0.1
            + stats[4] * 0.1
            + stats[5] * 6
            + stats[3]
        )
        if stats[0] >= 300:
            points += 5
        if stats[2] >= 100:
            points += 5
        if stats[4] >= 150:
            points += 5

        logger.warning(points)
        return points

    def extract_stats(labels, gameStats):
        stats = []
        stats.append(
            async_to_sync(get_value_at_index)(labels, "passingYards", gameStats)
        )
        stats.append(
            async_to_sync(get_value_at_index)(labels, "rushingAttempts", gameStats)
        )
        stats.append(
            async_to_sync(get_value_at_index)(labels, "rushingYards", gameStats)
        )
        stats.append(async_to_sync(get_value_at_index)(labels, "receptions", gameStats))
        stats.append(
            async_to_sync(get_value_at_index)(labels, "receivingYards", gameStats)
        )
        stats.append(
            async_to_sync(get_value_at_index)(labels, "rushingTouchdowns", gameStats)
            + async_to_sync(get_value_at_index)(labels, "passingTouchdowns", gameStats)
            + async_to_sync(get_value_at_index)(
                labels, "receivingTouchdowns", gameStats
            )
        )

        return stats
