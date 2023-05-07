from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('home/', include("player_scraping.urls"), name='index'),  
    path('accounts/', include("accounts.urls")), 
    path('admin/', admin.site.urls),    
]
