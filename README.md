# recetas
# He añadido al requirements.txt la libreria pillow para subir imagenes. No se si al final la usare en un futuro pero ahi esta.


# Clase User(Usuario).
# Nada diferente de lo que ya hemos hecho, con este modelo creamos nuestro Usuario con su username el cual será con el que se identificara dentro de la web
# y unos pocos datos más como la fecha de registro y una pequeña bio por si quiere decir algo de él.
class User(models.Model):
    username = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    date_joined = models.DateField(default=timezone.now)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username


# Clase Recipe(Receta).
# En este modelo nos permite crear nuestra receta con un titulo, una descripcion de como será, el autor que lo ha creado, la categoría a la que pertenece
# la fecha de creación, utensilios usados, y etiquetas. 
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #Relacion ManyToOne con user.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #Relacion ManyToMany ya que podemos tener varias categorias por receta.
    category = models.ManyToManyField('Category', blank=True)
# con el parametro "auto_add_now=True" se añade automaticamente la fecha y la hora de la creación.
    created = models.DateTimeField(auto_now_add=True)
    #Relaciones ManyToMany de Utensilios y Etiquetas
    utensils = models.ManyToManyField('Utensil', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    def __str__(self):
        return self.title
# Clase Ingredient(Ingrediente).
# En este modelo metemos las especificaciones de cada ingrediente que luego será usado en las recetas.
# Asi como una foto de cada uno
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    gluten_free = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)
    
    def __str__(self):
        return self.name

# Tabla ManyToMany entre Receta e Ingrediente.
# Esta es la tabla creada por mi con dos atributos nuevos. Que son la cantidad del ingrediente y la unidad del mismo.
# Ej: 200 g, 2 unidades,..
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.ingredient} en {self.recipe}"

# Clase Utensil(Utensilios).
# En este modelo se crean los utensilios que vamos a usar en cada receta, el material del que están hechos y si son
# compatibles con el lavavajillas como añadido.
class Utensil(models.Model):
    name = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    dishwasher_safe = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
# Clase Step(Paso).
# En este modelo se se crean los pasos que debe tener una receta. De cada receta se van poniendo los pasos uno a uno siempre
# con "PositiveInteger", asi no puede ser un numero negativo. Asi como lo que se tiene que hacer y el tiempo estimado de cada paso.
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    instruction = models.TextField()
    estimated_time = models.IntegerField()
    
    def __str__(self):
        return f"Paso {self.order} de {self.recipe}"
# Clase Category(Categoria).
# En este modelo añadimos las distintas categorias de recetas que habrá, con su descripción y una foto.
class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# Clase Comment(Comentario).
# este modelo añade comentarios a las recetas de cada usuario que quiera.
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario de {self.author.username} en {self.recipe.title}"

# Clase Tag(Etiqueta).
# este modelo guarda las etiquetas que pueden añadirse a las recetas.  A parte del nombre y de la descripción le ponemos un color 
# que se mostrara al final en nuestra web asi como un número que será las veces que se ha usado.
class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=20, default="green")
    description = models.TextField(blank=True)
    popularity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
# Clase Rating(Valoración).
# En este modelo se guarda la valoración de una usuario sobre una receta. 
# El atributo start guarda un numero entero el cual se almacena en una  lista de tuplas. En este caso con el choise le ponemos
# que el valor guardado será el mismo que el mostrado. Y un for con un rango del 1 al 5 que será nuestro rango de valoración.
# Tambien le añade un comentario y la fecha de creacion de la valoración. 
class Rating(models.Model):    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} dio {self.stars}★ a {self.recipe.title}"

# Clase ContactMessage(Mensaje de contacto).
# Un modelo que sirva de formulario de contacto para cualquier duda. EmailField() es una variante de CharField que valida
# automaticamente que sea un email con su formato. De no ser asi lanza un mensaje de error.
class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mensaje de {self.name}"

# Me di cuenta tarde que no habia relaciones OneToOne, si puede ser despues las añadire. Me puse a hacerlas y me di cuenta
# cuando estaba terminando el diagrama.