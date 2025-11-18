from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe>',views.view_recipe,name="recipe"),
    path('user/<int:user>',views.view_user,name="user"),
    path('ingredient/<int:ingredient>',views.view_ingredient,name="ingredient"),
    path('recipes/list',views.list_recipes,name='list_recipes'),
    path('recipes/url2/<int:year_recipe>/<int:month_recipe>', views.get_recipe_date,name='get_recipe_date'),
    path('recipes/url3/<str:theme>/', views.get_user_theme, name="get_user_theme"),
    path('category/<str:description>', views.get_category_recipe, name='get_category_recipe'),
    path('last-user-comment/<int:recipe>', views.get_last_user_recipe, name='get_last_user_recipe'),
    re_path(r'^filtro[0-9]$',views.recipes_no_comment,name='recipes_no_comment'),
    path('user/<int:id_author>/recipes',views.get_user,name='get_user'),
    path('get_recipe-ingredient',views.get_recipe_ingredient,name='get_recipe_ingredient'),
    path('get-recipe-name-description',views.get_recipe_name_description,name='get_recipe_name_description'),
    path('get-user-utensils',views.get_recipe_utensils,name="get_recipe_utensils"),
    path('recipes/list', views.list_recipes, name="list_recipes")
]
