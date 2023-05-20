# Generated by Django 4.2 on 2023-05-13 00:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("player_scraping", "0006_rename_team_player_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="abr_team",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="full_team",
            field=models.CharField(max_length=20, null=True),
        ),
    ]