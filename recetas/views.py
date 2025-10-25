from django.shortcuts import render
from .models import *
from django.db.models import Q, Prefetch

# Create your views here.
def index(request):
    return render(request, 'recetas/index.html', {})


def list_recipes(request):
    recipes=Recipe.objects.select_related("author").prefetch_related("recipe_ingredient__ingredient", "category").all()
    #recipes = (Recipe.objects.raw("SELECT * FROM recetas_recipe r "
     #                             + " JOIN recetas_user u ON r.user_id = u.id "
      #                            + " JOIN recetas_ingredient i ON i.ingredient_id = r.id "))
    return render(request, 'recipe/list.html',{"recipes_list":recipes})

def get_recipe_date(request, year_recipe, month_recipe):
    recipes=Recipe.objects.select_related("author").prefetch_related("recipe_ingredient", "category").all()
    recipes = recipes.all()
    recipes = recipes.filter(created__year=year_recipe, created__month=month_recipe)
    return render(request, 'recipe/url2.html',{"recipes_list":recipes})

def get_user_theme(request, theme):
    user = User.objects.select_related("usersettings")
    user = user.filter(Q(usersettings__theme=theme) | Q(usersettings__theme="dark")).order_by("date_joined")
    return render(request, 'recipe/url3.html', {"user_list":user})

def get_category_recipe(request, description):
    recipe = Recipe.objects.prefetch_related("category")
    recipe = recipe.filter(category__description__icontains=description)
    return render(request, 'recipe/url4.html', {'get_text':recipe})



def get_last_user_recipe(request, recipe):
    comment = Comment.objects.filter(recipe=recipe).select_related("author", "recipe").order_by('-created_at')[:1].get
    return render(request, 'user/url5.html',{"comment":comment})


def recipes_no_comment(request):
    recipe = Recipe.objects.select_related("author")
    recipe = recipe.filter(comment__isnull=True)
    return render(request, 'recipe/url6.html', {'no_comment': recipe})

def get_user(request, id_author):
    user = User.objects.prefetch_related("recipes").get(id=id_author)
    return render(request, 'user/url7.html',{'user': user})

