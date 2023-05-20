import json
import requests
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from django.core.management.base import BaseCommand
from player_scraping.models import Player
import logging


logger = logging.getLogger(__name__)


from player_scraping.models import Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Find all active players, fill player database and calculate points
        self.fetch_data_all(100)

    def fetch_player_details(self, player_id):
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

    def fetch_data_limit(self, limit, page, update_existing=False):
        url = f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit={limit}&page={page}"
        response = requests.get(url)
        json_data = response.json()

        player_ids = [player["id"] for player in json_data["items"] if player["active"]]

        if update_existing:
            existing_players = Player.objects.filter(id__in=player_ids).values_list(
                "id", flat=True
            )
            to_update = [player for player in player_ids if player in existing_players]
        else:
            to_update = player_ids

        with ThreadPoolExecutor(max_workers=20) as executor:
            new_player_details = list(
                executor.map(self.fetch_player_details, to_update)
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

    def fetch_data_all(self, limit, update_existing_only=False):
        count = self.fetch_data_limit(limit, 1, update_existing_only)

        total_pages = ceil(count / limit)

        for page in range(
            2, total_pages + 1
        ):  # start from 2 because we already fetched the first page
            self.fetch_data_limit(limit, page, update_existing_only)
