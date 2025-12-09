from django.contrib import admin
from .models import Recipe, User, Moderador, Ingredient, Utensil, Category, Tag

# Register your models here.
admin.site.register(Recipe)
admin.site.register(User)
admin.site.register(Moderador)
admin.site.register(Ingredient)
admin.site.register(Utensil)
admin.site.register(Category)
admin.site.register(Tag)