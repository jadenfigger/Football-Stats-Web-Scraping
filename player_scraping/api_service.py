import requests
import logging
from .models import Player
from concurrent.futures import ThreadPoolExecutor
from .exception_handler import APIException, DBException
from .stats_calculator import StatCalculator
from math import ceil

logger = logging.getLogger(__name__)


class APIService:
    @staticmethod
    def fetch_player_stats(player_id, week, season):
        # Fetch player stats from the API
        try:
            response = requests.get(
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?season={season}"
            )

            response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
            data = response.json()

            if data.get("categories") is None:
                logger.warning(
                    f"player data for {player_id} does not exist for the season {season}"
                )
                return None

            # find if the week exists
            for season_type in data["seasonTypes"]:
                if season_type["displayName"] == f"{season} Regular Season":
                    for category in season_type["categories"]:
                        if category["type"] == "event":
                            for game in category["events"]:
                                if data["events"][game["eventId"]]["week"] == week:
                                    logger.warning(game["stats"])
                                    logger.warning(data["names"])
                                    return StatCalculator.extract_stats(
                                        data["names"], game["stats"]
                                    )

            logger.warning(
                f"player data for {player_id} does not exist for the week {week}"
            )
            return None

        except requests.exceptions.HTTPError as errh:
            logger.warning(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.warning(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.warning(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logger.warning(f"Something went wrong: {err}")

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
            logger.warning(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.warning(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.warning(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logger.warning(f"Something went wrong: {err}")

    @staticmethod
    def fetch_data_limit(limit, page, update_existing):
        url = f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit={limit}&page={page}"
        logger.warning(url)
        logger.warning(page)
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
                executor.map(APIService.fetch_player_details, to_update)
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
    def fetch_data_all(limit, only_update_existing):
        count = APIService.fetch_data_limit(limit, 1, only_update_existing)

        total_pages = ceil(count / limit)

        if only_update_existing:
            Player.objects.all().delete()

        for page in range(
            2, total_pages + 1
        ):  # start from 2 because we already fetched the first page
            APIService.fetch_data_limit(limit, page, only_update_existing)
