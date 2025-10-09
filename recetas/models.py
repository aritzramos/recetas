from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    date_joined = models.DateField(default=timezone.now)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #Relacion ManyToOne con user.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #Relacion ManyToMany ya que podemos tener varias categorias por receta.
    category = models.ManyToManyField('Category', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    #Relaciones ManyToMany de Utensilios y Etiquetas
    utensils = models.ManyToManyField('Utensil', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    def __str__(self):
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    gluten_free = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
#Tabla ManyToMany entre Receta e Ingrediente.
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return self.quantity + self.unit + " de " + self.ingredient + " en " + self.recipe
    
class Utensil(models.Model):
    name = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    dishwasher_safe = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    instruction = models.TextField()
    estimated_time = models.IntegerField()
    
    def __str__(self):
        return "Paso " + self.order + " de " + self.recipe
    