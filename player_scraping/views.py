from .models import Player
from django.shortcuts import redirect, render
import logging

logger = logging.getLogger(__name__)


def home(request):
    # Get all players from the database
	
    p1 = Player(name="tom brady", position="QB")
    p1.save()
	
    players = Player.objects.all()
    
    # Render the home template with the players context variable
    return render(request, 'home.html')
	

def add_player(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the player name or ID from the request
        player_name = request.POST.get('player_name')
        player_id = request.POST.get('player_id')
        
        # Check if the player name was provided
        if player_name:
            # Search for the player in the database
            player = Player.objects.filter(name__icontains=player_name).first()
            
            # Check if the player was found
            if player:
                # Add the player to the user's roster
                # (assumes you have a Team model with a ForeignKey to the User model)
                request.user.team.players.add(player)
        # If the player ID was provided instead of the name
        elif player_id:
            # Get the player from the database
            player = Player.objects.get(pk=player_id)
            
            # Add the player to the user's roster
            # (assumes you have a Team model with a ForeignKey to the User model)
            request.user.team.players.add(player)
    
    # Redirect back to the home page
    return redirect('home')
