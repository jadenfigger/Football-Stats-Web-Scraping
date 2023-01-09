from django.db import models

class League(models.Model):
    name = models.CharField(max_length=100)
    number_of_teams = models.PositiveSmallIntegerField()
    current_week = models.PositiveSmallIntegerField()

class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    schedule = models.ManyToManyField('Game')
    roster = models.ManyToManyField('Player', related_name='teams')
    roster_history = models.ManyToManyField('Player', related_name='former_teams')

class Player(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    transaction_history = models.ManyToManyField('Transaction', related_name='players')

class Game(models.Model):
    home_team = models.ForeignKey('Team', related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey('Team', related_name='away_team', on_delete=models.CASCADE)
    week = models.PositiveSmallIntegerField()
    winner = models.ForeignKey('Team', related_name='winner', on_delete=models.CASCADE)
    date = models.DateField()

class Transaction(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    date = models.DateField()

class PlayerStat(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    points = models.PositiveSmallIntegerField()
    qb_points = models.PositiveSmallIntegerField()
    rb_points = models.PositiveSmallIntegerField()
    wr_points = models.PositiveSmallIntegerField()
