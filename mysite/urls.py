from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', )
    path('home/', include("player_scraping.urls"), name='index'),  # Changed name to "index"
    path('admin/', admin.site.urls),    
]
