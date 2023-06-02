from django.contrib import admin
from .models import Player, Team, League, Transaction, PlayerStat, TeamRoster, Match


# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(League)
admin.site.register(Transaction)
admin.site.register(PlayerStat)
admin.site.register(TeamRoster)
admin.site.register(Match)
