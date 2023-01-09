from . import views
from django.urls import path, include

urlpatterns = [
	path('', views.home, name="home"),
	path('add_player/', views.add_player, name='add_player'),
]