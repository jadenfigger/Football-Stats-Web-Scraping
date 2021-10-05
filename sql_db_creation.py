class sqlController:
	def __init__(self):
		self.league_loaded = False

		# Team name lists
		self.team_entry_values = []
		self.team_count_slider = None 
		# Team player id lists
		self.team_player_ids = {}
		self.player_id_entries = []
		# Total number of teams
		self.team_count = None

	def create_team_dict(self):
		for team in range(self.team_count):
			self.team_player_ids[self.team_entry_values[team]] = [self.player_id_entries[team][x].get() for x in range(12)]

		print(self.team_player_ids)
		
