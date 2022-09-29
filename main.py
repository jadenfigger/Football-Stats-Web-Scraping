from helper_functions import create_player_info, calculate_points
# nflTeamIds = ['buf', 'nwe', 'mia', 'nyj', 'cin', 'cle', 'pit', 'oti', 'htx', 'clt', 'jax', 'rai', 'den', 'kan', 'sdg', 'phi',
#               'was', 'dal', 'nyg', 'chi', 'min', 'gnb', 'det', 'car', 'tam', 'nor', 'atl', 'crd', 'ram', 'sea', 'sfo']

current_roster = {"JDOG": ["AlleJo02", "BarkSa00", "DiggSt00"], 
          "LOGANASAURUS": ["CarrDe02", "EkelAu00", "HillTy00"]}
week = 3
final_points = {}

def main():
    for team_name, players in current_roster.items():
        QB_points = calculate_points(players[0], "qb", week)
        RB_points = calculate_points(players[1], "rb", week)
        WR_points = calculate_points(players[2], "wr", week)

        final_points.update({team_name: [QB_points, RB_points, WR_points]})


if (__name__ == "__main__"):
    main() 
