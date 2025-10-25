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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/',  blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[("light", "claro"), ("dark", "oscuro")], default="light")
    notifications_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Configuracion de {self.user.username}"
    
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_recipes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    reputation = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Estadisticas de {self.user.username}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    gluten_free = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #Relacion ManyToOne con user.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    #Relacion ManyToMany ya que podemos tener varias categorias por receta.
    category = models.ManyToManyField('Category', blank=True)
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    created = models.DateTimeField(auto_now_add=True)
    #Relaciones ManyToMany de Utensilios y Etiquetas
    utensils = models.ManyToManyField('Utensil', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    def __str__(self):
        return self.title
    
#Tabla ManyToMany entre Receta e Ingrediente.
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredient', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.ingredient} en {self.recipe}"
    
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
        return f"Paso {self.order} de {self.recipe}"

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario de {self.author.username} en {self.recipe.title}"

class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=20, default="green")
    description = models.TextField(blank=True)
    popularity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Rating(models.Model):    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} dio {self.stars}★ a {self.recipe.title}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mensaje de {self.name}"
    