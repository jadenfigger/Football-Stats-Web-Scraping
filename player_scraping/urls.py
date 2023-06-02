from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.home, name="index"),
    path("my_team/", views.my_team, name="my_team"),
    path("change_roster/", views.change_roster, name="change_roster"),
    path("drop_player/<str:player_id>/", views.drop_player, name="drop_player"),
    path("set_lineup/", views.set_lineup, name="set_lineup"),
    path(
        "trade_player/<str:player_id>/<str:player_to_drop_id>/",
        views.trade_player,
        name="trade_player",
    ),
    path("search/", views.search, name="search"),  # Add this line
]
