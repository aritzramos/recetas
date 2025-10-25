from django.shortcuts import render
from .models import *
from django.db.models import Q, Prefetch, F, Avg,Max,Min,Count
from django.views.defaults import page_not_found

# Create your views here.
def my_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def my_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def my_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def my_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

def index(request):
    return render(request, 'recetas/index.html', {})

# Devuelve todas las recetas con categorias y su autor.
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

# Devuelve las recetas que se hayan publicado en octubre de 2025
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

# Devuelve los usuarios que tengan el tema en oscuro.
def get_user_theme(request, theme):
    user = User.objects.select_related("usersettings")
    user = user.filter(Q(usersettings__theme=theme) | Q(usersettings__theme="dark")).order_by("date_joined")
    return render(request, 'recipe/url3.html', {"user_list":user})
"""SELECT u.*, us.*
FROM recetas_user u
LEFT JOIN recetas_usersettings us ON u.id = us.user_id
WHERE us.theme = '{theme}' OR us.theme = 'dark'
ORDER BY u.date_joined ASC;"""

# Devuelve las recetas que en la descripcion de categoria incluya "Servicio"
def get_category_recipe(request, description):
    recipe = Recipe.objects.prefetch_related("category")
    recipe = recipe.filter(category__description__icontains=description)
    return render(request, 'recipe/url4.html', {'get_text':recipe})
"""SELECT r.*, c.*
FROM recetas_recipe r
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id
WHERE c.description ILIKE '%{description}%';"""


# Devuelve el usuario que ha comentado el ultimo en una receta
# Aqui he usado firts en vez del codigo dado en clase ya que me lanzaba más querys de las que yo queria.
# lo que hace first al final es obtenernos el primer objeto de la Query, asi que al estar ordenado nos devuelve
# lo que queremos.
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

# Devuelve las recetas que no tienen comentarios
def recipes_no_comment(request):
    recipe = Recipe.objects.select_related("author")
    recipe = recipe.filter(comment__isnull=True)
    return render(request, 'recipe/url6.html', {'no_comment': recipe})
"""SELECT r.*, u.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_comment c ON c.recipe_id = r.id
WHERE c.id IS NULL;"""

# Devuelve las recetas de cada usuario
def get_user(request, id_author):
    user = User.objects.prefetch_related(Prefetch("recipes")).get(id=id_author)
    return render(request, 'user/url7.html',{'user': user})
"""SELECT u.*, r.*
FROM recetas_user u
LEFT JOIN recetas_recipe r ON r.author_id = u.id
WHERE u.id = {id_author};"""

# Devuelve las recetas que tengan un ingrediente "gluten free"
def get_recipe_ingredient(request):
    recipe = Recipe.objects.prefetch_related("recipe_ingredient")
    recipe = recipe.filter(ingredient__gluten_free=1)
    return render(request, 'recipe/url8.html', {'recipe': recipe})
"""SELECT r.*, ri.*, i.*
FROM recetas_recipe r
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
WHERE i.gluten_free = TRUE;"""

# Devuelve las recetas que en su descripcion contengan el titulo de la misma
def get_recipe_name_description(request):
    recipe = Recipe.objects.select_related("author")
    recipe = recipe.filter(description__contains=F("title"))
    return render(request, 'recipe/url9.html',{'recipe': recipe})
"""SELECT r.*, u.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
WHERE r.description LIKE CONCAT('%', r.title, '%');"""

# Devuelve los utensilios de cada receta y hace una media de todos los utensilios por receta,
# los utensilios maximos en una receta y los minimos.
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