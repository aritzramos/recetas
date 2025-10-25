from django.shortcuts import render
from .models import *
from django.db.models import Q, Prefetch, F, Avg,Max,Min,Count

# Create your views here.
def index(request):
    return render(request, 'recetas/index.html', {})


def list_recipes(request):
    recipes=Recipe.objects.select_related("author").prefetch_related("category")
    return render(request, 'recipe/list.html',{"recipes_list":recipes})
"""SELECT r.*, u.*, ri.*, i.*, c.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id;"""

def get_recipe_date(request, year_recipe, month_recipe):
    recipes=Recipe.objects.select_related("author").prefetch_related("category")
    recipes = recipes.filter(created__year=year_recipe, created__month=month_recipe)
    return render(request, 'recipe/url2.html',{"recipes_list":recipes})
"""SELECT r.*, u.*, ri.*, i.*, c.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id
WHERE EXTRACT(YEAR FROM r.created) = {year_recipe}
  AND EXTRACT(MONTH FROM r.created) = {month_recipe};"""

def get_user_theme(request, theme):
    user = User.objects.select_related("usersettings")
    user = user.filter(Q(usersettings__theme=theme) | Q(usersettings__theme="dark")).order_by("date_joined")
    return render(request, 'recipe/url3.html', {"user_list":user})
"""SELECT u.*, us.*
FROM recetas_user u
LEFT JOIN recetas_usersettings us ON u.id = us.user_id
WHERE us.theme = '{theme}' OR us.theme = 'dark'
ORDER BY u.date_joined ASC;"""

def get_category_recipe(request, description):
    recipe = Recipe.objects.prefetch_related("category")
    recipe = recipe.filter(category__description__icontains=description)
    return render(request, 'recipe/url4.html', {'get_text':recipe})
"""SELECT r.*, c.*
FROM recetas_recipe r
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id
WHERE c.description ILIKE '%{description}%';"""


def get_last_user_recipe(request, recipe):
    comment = Comment.objects.filter(recipe=recipe).select_related("author", "recipe").order_by('-created_at').first()
    return render(request, 'user/url5.html',{"comment":comment})
"""SELECT c.*, u.*, r.*
FROM recetas_comment c
JOIN recetas_user u ON c.author_id = u.id
JOIN recetas_recipe r ON c.recipe_id = r.id
WHERE c.recipe_id = {recipe_id}
ORDER BY c.created_at DESC
LIMIT 1;"""

def recipes_no_comment(request):
    recipe = Recipe.objects.select_related("author")
    recipe = recipe.filter(comment__isnull=True)
    return render(request, 'recipe/url6.html', {'no_comment': recipe})
"""SELECT r.*, u.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_comment c ON c.recipe_id = r.id
WHERE c.id IS NULL;"""

def get_user(request, id_author):
    user = User.objects.prefetch_related(Prefetch("recipes")).get(id=id_author)
    return render(request, 'user/url7.html',{'user': user})
"""SELECT u.*, r.*
FROM recetas_user u
LEFT JOIN recetas_recipe r ON r.author_id = u.id
WHERE u.id = {id_author};"""

def get_recipe_ingredient(request):
    recipe = Recipe.objects.prefetch_related("recipe_ingredient")
    recipe = recipe.filter(ingredient__gluten_free=1)
    return render(request, 'recipe/url8.html', {'recipe': recipe})
"""SELECT r.*, ri.*, i.*
FROM recetas_recipe r
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
WHERE i.gluten_free = TRUE;"""

def get_recipe_name_description(request):
    recipe = Recipe.objects.select_related("author")
    recipe = recipe.filter(description__contains=F("title"))
    return render(request, 'recipe/url9.html',{'recipe': recipe})
"""SELECT r.*, u.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
WHERE r.description LIKE CONCAT('%', r.title, '%');"""

def get_recipe_utensils(request):
    count_utensils = Recipe.objects.annotate(num_utensils=Count("utensils"))
    stats = count_utensils.aggregate(
    average = Avg("num_utensils"),
    maximum = Max("num_utensils"),
    minimum = Min("num_utensils")
    )
    return render(request, 'recipe/url10.html',{"average":stats["average"],"maximum":stats["maximum"],"minimum":stats["minimum"], "recipe": count_utensils})
"""SELECT r.id, r.title, COUNT(ru.utensil_id) AS num_utensils
FROM recetas_recipe r
LEFT JOIN recetas_recipe_utensils ru ON ru.recipe_id = r.id
GROUP BY r.id;

Estadisticas:

SELECT AVG(sub.num_utensils) AS average,
       MAX(sub.num_utensils) AS maximum,
       MIN(sub.num_utensils) AS minimum
FROM (
    SELECT r.id, COUNT(ru.utensil_id) AS num_utensils
    FROM recetas_recipe r
    LEFT JOIN recetas_recipe_utensils ru ON ru.recipe_id = r.id
    GROUP BY r.id
) AS sub;"""