from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/list',views.list_recipes,name='list_recipes'),
    path('recipes/url2/<int:year_recipe>/<int:month_recipe>', views.get_recipe_date,name='get_recipe_date'),
    path('recipes/url3/<str:theme>/', views.get_user_theme, name="get_user_theme")
]
