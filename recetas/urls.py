from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/list',views.list_recipes,name='list_recipes'),
]
