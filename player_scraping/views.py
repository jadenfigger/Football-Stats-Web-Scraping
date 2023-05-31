from .models import Player, Team, League, PlayerStat, TeamRoster
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .services import PlayerDataService, PlayerPointsService
from .forms import WeekSelectForm
import logging

logger = logging.getLogger(__name__)


@login_required
def home(request):
    team = Team.objects.filter(owner=request.user).first()
    roster = team.roster.all() if team else []
    current_season = 2022  # Assuming season is an integer
    form = WeekSelectForm(request.POST or None)

    context = {"form": form}
    # Handle the form
    if request.method == "POST":
        if form.is_valid():
            current_week = int(form.cleaned_data["week"])
        else:
            current_week = League.objects.first().current_week
    else:
        current_week = League.objects.first().current_week

    context["roster_with_points"] = []
    for player in roster:
        player_points = PlayerDataService.get_player_points(
            player, current_week, current_season
        )
        context["roster_with_points"].append((player, player_points))

    logger.warning(context)
    return render(request, "index.html", context)


@login_required
def my_team(request):
    roster_with_points = PlayerDataService.get_player_roster_with_points(request)

    return render(request, "my_team.html", {"roster_with_points": roster_with_points})


def change_roster(request):
    if request.method == "POST":
        # Process roster changes based on submitted form data
        # You will need to update your models and write the logic for changing the roster here

        # Redirect back to the index page after processing the roster changes
        return redirect("index")

    # If request.method is not POST, redirect to the index page
    return redirect("index")


@login_required
def search(request):
    if request.method == "GET":
        search_query = request.GET.get("q", "")
        players = Player.objects.filter(name__icontains=search_query)[:5]
        player_data = [
            {"id": player.id, "name": player.name, "position": player.position}
            for player in players
        ]
        return JsonResponse({"players": player_data})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@login_required
def add_player_to_team(request, player_id, player_to_drop_id=None):
    logger.warning(f"Received player_id: {player_id}")
    logger.warning(f"Request user: {request.user}")
    try:
        player = Player.objects.get(id=player_id)
        team = Team.objects.get(owner=request.user)

        if player_to_drop_id:
            player_to_drop = Player.objects.get(id=player_to_drop_id)
            if player_to_drop in team.roster.all():
                team.roster.remove(player_to_drop)
            else:
                return JsonResponse(
                    {"success": False, "error": "Player to drop not found in the team"}
                )

        # You can add a condition here to decide whether to add the player to the starting roster or backup roster.
        # For this example, I am adding the player to the starting roster.
        team.roster.add(player)
        team.save()
        player_dict = model_to_dict(player)
        return JsonResponse({"success": True, "player": player_dict})
    except (Player.DoesNotExist, Team.DoesNotExist):
        return JsonResponse({"success": False, "error": "Invalid request"})


def trade_player(request):
    if request.method == "POST":
        # Process player addition based on submitted form data
        # You will need to update your models and write the logic for adding a player here

        # Redirect back to the my_team page after processing the player addition
        return redirect("my_team")

    # If request.method is not POST, redirect to the my_team page
    return redirect("my_team")


def set_lineup(request):
    if request.method == "POST":
        # Process lineup setting based on submitted form data
        # You will need to update your models and write the logic for setting the lineup here

        # Redirect back to the my_team page after processing the lineup setting
        return redirect("my_team")

    # If request.method is not POST, redirect to the my_team page
    return redirect("my_team")


def drop_player(request, player_id):
    try:
        team = Team.objects.get(owner=request.user)
        player = Player.objects.get(id=player_id)
        if player in team.starting_roster.all():
            team.starting_roster.remove(player)
        elif player in team.backup_roster.all():
            team.backup_roster.remove(player)
        else:
            return JsonResponse(
                {"success": False, "error": "Player to drop not found in the team"}
            )

        team.save()
        return JsonResponse({"success": True})
    except (Player.DoesNotExist, Team.DoesNotExist):
        return JsonResponse({"success": False, "error": "Invalid request"})


def fetch_player_data(request, player_id):
    result = PlayerDataService.fetch_data(player_id, "2022")
    if isinstance(result, str):
        return JsonResponse({"message": result}, status=500)
    else:
        return JsonResponse({"message": "Player data fetched successfully"})


def calculate_player_points(request, player_id, season, week):
    points = PlayerPointsService.calculate_points(player_id, season, week)
    if isinstance(points, str):
        return JsonResponse({"message": points}, status=404)
    else:
        return JsonResponse({"points": points})
