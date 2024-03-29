# Generated by Django 4.1.2 on 2023-01-03 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('player_scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number_of_teams', models.PositiveSmallIntegerField()),
                ('current_week', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='player_id',
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_scraping.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_scraping.team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='roster',
            field=models.ManyToManyField(related_name='teams', to='player_scraping.player'),
        ),
        migrations.AddField(
            model_name='team',
            name='roster_history',
            field=models.ManyToManyField(related_name='former_teams', to='player_scraping.player'),
        ),
        migrations.AddField(
            model_name='team',
            name='schedule',
            field=models.ManyToManyField(to='player_scraping.game'),
        ),
        migrations.CreateModel(
            name='PlayerStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=20)),
                ('points', models.PositiveSmallIntegerField()),
                ('qb_points', models.PositiveSmallIntegerField()),
                ('rb_points', models.PositiveSmallIntegerField()),
                ('wr_points', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_scraping.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_scraping.player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='player_scraping.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='player_scraping.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='player_scraping.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='player_scraping.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='transaction_history',
            field=models.ManyToManyField(related_name='players', to='player_scraping.transaction'),
        ),
    ]
