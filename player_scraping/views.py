from .models import Player, Team, League
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .forms import WeekSelectForm, TradePlayerForm
from .db_service import DBService
import logging

logger = logging.getLogger(__name__)


@login_required
def home(request):
    context = {}
    context.update(DBService.get_player_roster_with_points(request))
    context.update(DBService.get_weeks_schedule(context["current_week"]))

    logger.warning(f"context: {context}")
    return render(request, "index.html", context)


@login_required
def my_team(request):
    context = {}
    # context.update(
    #     DBService.propose_transaction()
    # )  # eventually move propose_transaction to separate file
    # if request.method == "POST":
    #     form = TradePlayerForm(request.POST, user=request.user)
    #     if form.is_valid():
    #         player_to_add = request.POST.get("player_to_add")
    #         player_to_drop = form.cleaned_data["player_to_drop"]

    #         # Here you would add the logic to trade the players
    #         trade_players(player_to_add, player_to_drop)

    #         return JsonResponse({"success": True})
    #     else:
    #         return JsonResponse({"error": "Invalid form data"}, status=400)
    # else:
    #     form = TradePlayerForm(user=request.user)

    # return render(request, "trade_player.html", {"form": form})

    form = TradePlayerForm(request.POST or None)
    context = {"form": form}
    context.update(DBService.get_player_roster_with_points(request))

    return render(request, "my_team.html", context=context)


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
def trade_player(request, player_id, player_to_drop_id):
    logger.warning(f"Received player_id: {player_id}")
    logger.warning(f"Request user: {request.user}")
    try:
        player = Player.objects.get(id=player_id)
        team = Team.objects.get(owner=request.user)

        if player_to_drop_id and player_id:
            player_to_drop = Player.objects.get(id=player_to_drop_id)
            if player_to_drop in team.roster.all():
                team.roster.remove(player_to_drop)
            else:
                return JsonResponse(
                    {"success": False, "error": "Player to drop not found in the team"}
                )


        team.roster.add(player)
        team.save()
        player_dict = model_to_dict(player)
        return JsonResponse({"success": True, "player": player_dict})
    except (Player.DoesNotExist, Team.DoesNotExist):
        return JsonResponse({"success": False, "error": "Invalid request"})


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
