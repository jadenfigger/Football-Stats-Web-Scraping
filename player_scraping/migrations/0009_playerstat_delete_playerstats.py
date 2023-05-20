# Generated by Django 4.2 on 2023-05-16 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "player_scraping",
            "0008_playerstats_remove_player_points_delete_playerstat_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerStat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season", models.IntegerField()),
                ("week", models.IntegerField()),
                ("passingYards", models.IntegerField()),
                ("rushingAttempts", models.IntegerField()),
                ("rushingYards", models.IntegerField()),
                ("touchdowns", models.IntegerField()),
                ("receivingYards", models.IntegerField()),
                ("receptions", models.IntegerField()),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stats",
                        to="player_scraping.player",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PlayerStats",
        ),
    ]