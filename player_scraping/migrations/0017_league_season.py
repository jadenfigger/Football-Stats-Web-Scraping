# Generated by Django 4.2 on 2023-06-01 23:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "player_scraping",
            "0016_alter_match_team1_points_alter_match_team2_points_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="league",
            name="season",
            field=models.IntegerField(null=True),
        ),
    ]
