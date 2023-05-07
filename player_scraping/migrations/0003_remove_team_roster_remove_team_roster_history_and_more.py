# Generated by Django 4.2 on 2023-05-07 23:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("player_scraping", "0002_game_league_team_remove_player_player_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="roster",
        ),
        migrations.RemoveField(
            model_name="team",
            name="roster_history",
        ),
        migrations.AddField(
            model_name="team",
            name="backup_roster",
            field=models.ManyToManyField(
                related_name="backup_teams", to="player_scraping.player"
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="starting_roster",
            field=models.ManyToManyField(
                related_name="starting_teams", to="player_scraping.player"
            ),
        ),
    ]
