from django.urls import path

from .api_views import *

urlpatterns = [
    path('recipes', recipe_list_api),
    path('recipess', recipe_list_api_mejorado),
]