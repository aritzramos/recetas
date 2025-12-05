from django.contrib import admin
from .models import Recipe, User, Moderador

# Register your models here.
admin.site.register(Recipe)
admin.site.register(User)
admin.site.register(Moderador)