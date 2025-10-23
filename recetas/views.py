from django.shortcuts import render
from .models import *
from django.db.models import Q

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

def get_recipe_date(request, year_recipe, month_recipe):
    recipes=Recipe.objects.select_related("author").prefetch_related("recipe_ingredient", "category")
    recipes = recipes.all()
    recipes = recipes.filter(created__year=year_recipe, created__month=month_recipe)
    return render(request, 'recipe/url2.html',{"recipes_list":recipes})

def get_user_theme(request, theme):
    user = User.objects.select_related("usersettings")
    user = user.filter(Q(usersettings__theme=theme) | Q(usersettings__theme="dark")).order_by("date_joined")
    return render(request, 'recipe/url3.html', {"user_list":user})