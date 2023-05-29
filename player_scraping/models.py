from django.db import models


class League(models.Model):
    name = models.CharField(max_length=100)
    number_of_teams = models.PositiveSmallIntegerField()
    current_week = models.PositiveSmallIntegerField()


class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    roster = models.ManyToManyField("Player", related_name="starting_teams")
    league = models.ForeignKey("League", null=True, on_delete=models.CASCADE)


class Player(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20)
    full_team = models.CharField(max_length=20, null=True)
    abr_team = models.CharField(max_length=5, null=True)
    transaction_history = models.ManyToManyField("Transaction", related_name="players")


# A real-time reference of the player stats for a player in a particular week/season
class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="stats")
    season = models.IntegerField()
    week = models.IntegerField()
    points = models.DecimalField(
        null=True, decimal_places=2, max_digits=6
    )  # Store the points calculated based on real-life performances
    # You can add more stats if you want


# A final reference for each player on a team for each week in a season.
class TeamRoster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    week = models.IntegerField()
    season = models.IntegerField()
    points = models.DecimalField(
        null=True, decimal_places=2, max_digits=6
    )  # Store the points that will be added to the team's score
    is_starting = models.BooleanField(
        default=True
    )  # True for starting players, False for backups


class Match(models.Model):
    team1 = models.ForeignKey(Team, related_name="team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="team2", on_delete=models.CASCADE)
    league = models.ForeignKey(
        "League", related_name="league", on_delete=models.CASCADE
    )
    week = models.IntegerField()
    season = models.IntegerField()
    team1_points = models.DecimalField(
        null=True, decimal_places=2, max_digits=6
    )  # Store the total points of team1 in this match
    team2_points = models.DecimalField(
        null=True, decimal_places=2, max_digits=6
    )  # Store the total points of team2 in this match


class Transaction(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    date = models.DateField()
