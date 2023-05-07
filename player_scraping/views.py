from .models import Player, Team
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Team
import logging

logger = logging.getLogger(__name__)

def home(request):
    # Get all players from the database

    p1 = Player(name="tom brady", position="QB")
    p1.save()

    players = Player.objects.all()

    # Render the home template with the players context variable
    return render(request, 'index.html', {'players': players})  # Pass the players variable to the template


@login_required
def my_team(request):
    # Retrieve the user's team based on the owner
    user_team = Team.objects.get(owner=request.user)

    # Get the roster for the user's team
    roster = user_team.roster.all()

    return render(request, 'my_team.html', {'roster': roster})


def change_roster(request):
    if request.method == 'POST':
        # Process roster changes based on submitted form data
        # You will need to update your models and write the logic for changing the roster here

        # Redirect back to the index page after processing the roster changes
        return redirect('index')

    # If request.method is not POST, redirect to the index page
    return redirect('index')

@login_required
def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('q', '')
        players = Player.objects.filter(name__icontains=search_query)[:5]
        player_data = [{'id': player.id, 'name': player.name, 'position': player.position} for player in players]
        return JsonResponse({'players': player_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def add_player_to_team(request, player_id):
    logger.warning(f"Received player_id: {player_id}")
    logger.warning(f"Request user: {request.user}")
    try:
        player = Player.objects.get(id=player_id)
        team = Team.objects.get(owner=request.user)
        team.roster.add(player)
        team.save()
        return JsonResponse({'success': True})
    except (Player.DoesNotExist, Team.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Invalid request'})


def trade_player(request):
    if request.method == 'POST':
        # Process player addition based on submitted form data
        # You will need to update your models and write the logic for adding a player here

        # Redirect back to the my_team page after processing the player addition
        return redirect('my_team')

    # If request.method is not POST, redirect to the my_team page
    return redirect('my_team')

def set_lineup(request):
    if request.method == 'POST':
        # Process lineup setting based on submitted form data
        # You will need to update your models and write the logic for setting the lineup here

        # Redirect back to the my_team page after processing the lineup setting
        return redirect('my_team')

    # If request.method is not POST, redirect to the my_team page
    return redirect('my_team')