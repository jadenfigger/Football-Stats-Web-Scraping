from lib2to3.pytree import Base
from urllib.error import HTTPError
from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from math import ceil
import logging

logger = logging.getLogger(__name__)


from player_scraping.models import Player

class Command(BaseCommand):

	def handle(self, *args, **options):
		# count = fetch_data_all(100, self)
		fill_positions(self)



def fill_positions(commandLink):
	for player in Player.objects.all():
		player_id = player.player_id
		logger.warning(player_id)
		player_json_data = json.loads(BeautifulSoup(urlopen(f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}"), "html.parser").text)


		player_position = player_json_data['athlete']['position']['abbreviation']
		player.position = player_position
		player.save()
		commandLink.stdout.write(f"{player.name} update with position {player_position}")


def fetch_data_limit(limit, page, commandLink):
	player_urls = {}

	try:
		html = urlopen(f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit={limit}&page={page}&active=true")
	except:
		CommandError(f"Could not load url with limit: {limit} and page: {page}")


	json_data = json.loads(html.read().decode("utf-8"))

	for player in json_data['items']:
		if player['active']:
			player_id = player['id']
			player_name = player['fullName']
			
			try:
				player_json_data = json.loads(urlopen(f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}").read().decode("utf-8"))
			except HTTPError:
				continue

			player_position = player_json_data['athlete']['position']['abbreviation']
			
			if (player_position == "QB" or player_position == "RB" or player_position == "WR"):
				obj, created = Player.objects.get_or_create(player_id=player_id, name=player_name)
				if (created):
					commandLink.stdout.write(commandLink.style.SUCCESS(f"{player_name} Saved"))
					obj.save()
			else:
				commandLink.stdout.write(commandLink.style.WARNING(f"{player_name} not valid"))

	return json_data['count']

def fetch_data_all(limit, commandLink):
	count = fetch_data_limit(limit, 30, commandLink)

	for page in range(1, ceil(count/limit)):
		commandLink.stdout.write(f"Page Count: {page}")
		n_count = fetch_data_limit(limit, page, commandLink)
