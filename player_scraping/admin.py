from django.contrib import admin
from .models import Player, Team, Game, League, Transaction, PlayerStat


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "position")


# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Transaction)
admin.site.register(PlayerStat)
