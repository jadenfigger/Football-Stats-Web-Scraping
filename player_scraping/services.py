import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from .models import Player, PlayerStat
from .utils import get_value_at_index


logger = logging.getLogger(__name__)


class PlayerDataService:
    @staticmethod
    def fetch_player_stats(player_id, week, season):
        # Fetch player stats from the API
        try:
            response = requests.get(
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?season={season}"
            )
            logger.warning(
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?season={season}"
            )
            response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
            data = response.json()

            if data.get("categories") is None:
                logger.warning(
                    f"{player_id} does not exist for the season year: {season}"
                )
                return None

            # find if the week exists
            eventId = None
            for season_type in data["seasonTypes"]:
                if season_type["displayName"] == f"{season} Regular Season":
                    for category in season_type["categories"]:
                        if category["type"] == "event":
                            for game in category["events"]:
                                if data["events"][game["eventId"]]["week"] == week:
                                    return PlayerPointsService.extract_stats(
                                        data["names"], game["stats"]
                                    )

            logger.warning(f"{player_id} does not exist for the week: {week}")
            return None

        except requests.exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logger.error(f"Something went wrong: {err}")

    @staticmethod
    def save_player_stats(player_id, week, season, data):
        # Save player stats to the database
        if data:
            player = Player.objects.get(id=player_id)

            points = PlayerPointsService.calculate_points(data)
            PlayerStat.objects.update_or_create(
                player=player,
                season=season,
                week=week,
                points=points,
            )

        return True

    @staticmethod
    def fetch_and_save_player_stats(player_id, week, season):
        # Fetch player stats from the API and save them to the database
        data = PlayerDataService.fetch_player_stats(player_id, week, season)
        if data is not None:
            PlayerDataService.save_player_stats(player_id, week, season, data)

    # Will get the player points based on player_id, week, and season. If the playerStat does not exist then will create one.
    @staticmethod
    def get_player_points(player, week, season):
        player_stat = PlayerStat.objects.filter(
            player=player, week=week, season=season
        ).first()
        if player_stat:
            return player_stat.points
        else:
            return PlayerDataService.fetch_and_save_player_stats(
                player.id, week, season
            )

    @staticmethod
    def fetch_player_details(player_id):
        # Fetch player details from the API
        try:
            url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}"
            response = requests.get(url)
            response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
            player_json_data = response.json()
            return player_json_data
        except requests.exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logger.error(f"Something went wrong: {err}")

    @staticmethod
    def fetch_data_limit(limit, page, update_existing=False):
        url = f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit={limit}&page={page}"
        response = requests.get(url)
        json_data = response.json()

        player_ids = [player["id"] for player in json_data["items"] if player["active"]]

        to_update = set(player_ids)
        if update_existing:
            existing_players = set(
                Player.objects.filter(id__in=player_ids).values_list("id", flat=True)
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

        Player.objects.bulk_create(players_to_create, ignore_conflicts=True)

        return json_data["count"]

    @staticmethod
    def fetch_data_all(limit, update_existing=True, add_and_update=False):
        count = PlayerDataService.fetch_data_limit(limit, 1, update_existing)

        total_pages = ceil(count / limit)

        for page in range(
            2, total_pages + 1
        ):  # start from 2 because we already fetched the first page
            if add_and_update:
                # if add_and_update is True, we want to update existing players and add new players
                PlayerDataService.fetch_data_limit(limit, page, update_existing=True)
            else:
                # otherwise, we respect the update_existing parameter
                PlayerDataService.fetch_data_limit(limit, page, update_existing)


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
        stats.append(get_value_at_index(labels, "passingYards", gameStats))
        stats.append(get_value_at_index(labels, "rushingAttempts", gameStats))
        stats.append(get_value_at_index(labels, "rushingYards", gameStats))
        stats.append(get_value_at_index(labels, "receptions", gameStats))
        stats.append(get_value_at_index(labels, "receivingYards", gameStats))
        stats.append(
            get_value_at_index(labels, "rushingTouchdowns", gameStats)
            + get_value_at_index(labels, "passingTouchdowns", gameStats)
            + get_value_at_index(labels, "receivingTouchdowns", gameStats)
        )

        return stats
