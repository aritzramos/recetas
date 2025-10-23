from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, 'recetas/index.html', {})


def list_recipes(request):
    recipes=Recipe.objects.select_related("author").prefetch_related("recipe_ingredient", "category")
    recipes = recipes.all()
    #recipes = (Recipe.objects.raw("SELECT * FROM recetas_recipe r "
     #                             + " JOIN recetas_user u ON r.user_id = u.id "
      #                            + " JOIN recetas_ingredient i ON i.ingredient_id = r.id "))
    return render(request, 'recipe/list.html',{"recipes_list":recipes})

