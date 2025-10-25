from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, 'recetas/index.html', {})


def list_recipes(request):
    recipes=Recipe.objects.select_related("author").prefetch_related("category")
    return render(request, 'recipe/list.html',{"recipes_list":recipes})
<<<<<<< HEAD

def get_recipe_date(request, year_recipe, month_recipe):
    recipes=Recipe.objects.select_related("author").prefetch_related("recipe_ingredient", "category")
    recipes = recipes.all()
    recipes = recipes.filter(created__year=year_recipe, created__month=month_recipe)
    return render(request, 'recipe/url2.html',{"recipes_list":recipes})
=======
"""SELECT r.*, u.*, ri.*, i.*, c.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id;"""
>>>>>>> url1
