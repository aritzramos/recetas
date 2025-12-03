from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q, Prefetch, F, Avg,Max,Min,Count
from django.views.defaults import page_not_found
from django.contrib import messages
from datetime import datetime

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

# =================================================================
# Vistas de Lectura (Read) de Entidades
# =================================================================

# Detalles de una sola receta
def view_recipe(request, recipe):
    recipes = Recipe.objects.select_related("author").prefetch_related("category", "utensils", "tags", Prefetch('ingredient')).get(id=recipe)
    return render(request, 'recipe/mostrar_recipe.html',{"recipe": recipes})

# Detalles de un solo usuario
def view_user(request, user):
    user =  User.objects.get(id=user)
    return render(request, 'user/mostrar_user.html',{"user":user})

# Detalles de un solo ingrediente
def view_ingredient(request, ingredient):
    ingredient =  Ingredient.objects.get(id=ingredient)
    return render(request, 'ingredient/mostrar_ingredient.html',{"ingredient":ingredient})

# Detalles de un solo utensilio
def view_utensil(request, utensil):
    utensil =  Utensil.objects.get(id=utensil)
    return render(request, 'utensil/mostrar_utensil.html',{"utensil":utensil})

# Detalles de una sola categoria
def view_category(request, category):
    category =  Category.objects.get(id=category)
    return render(request, 'category/mostrar_category.html',{"category":category})

# Detalles de una sola etiqueta
def view_tag(request, tag):
    tag =  Tag.objects.get(id=tag)
    return render(request, 'tag/mostrar_tag.html',{"tag":tag})

# =================================================================
# Vistas de Creación y Modificación de Recetas (CRUD: Create/Update)
# =================================================================

# Vista principal para crear una nueva receta (maneja formulario GET/POST)
def create_recipe(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    formData = None
    if request.method == "POST":
        formData = request.POST
        
    form = RecipeModelForm(formData)
    
    if (request.method == "POST"):
        
        recipe_create = create_recipe_model(form)
        if(recipe_create):
            messages.success(request, 'Se ha creado la receta correctamente.')
            return redirect('list_recipes')
    return render(request, 'recipe/create_recipe_bootstrap.html',{"form": form})

# Función auxiliar para guardar una nueva receta en la base de datos
def create_recipe_model(form):
    recipe_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            recipe_create = True
        except Exception as error:
            print(error)
            pass
    return recipe_create

# ==================================================================================
# Vista para actualizar/editar una receta existente (carga instancia para editar)
# ==================================================================================

def recipe_update(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    
    datesForm = None
    
    if request.method == "POST":
        datesForm = request.POST
    
    form = RecipeModelForm(datesForm,instance=recipe)
    
    if (request.method == "POST"):
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se ha editado la receta correctamente")
                return redirect('list_recipes')
            except Exception as error:
                print(error)
    return render(request, 'recipe/updateRecipe.html',{'form': form,'recipe':recipe})
 
# =================================================================
# Vistas de Eliminación de Recetas (CRUD: Delete)
# =================================================================

def recipe_delete(request,recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    try:
        recipe.delete()
        messages.success(request, "Se ha elimnado la receta correctamente")
    except:
        pass
    return redirect('list_recipes')

# =================================================================
# Vistas de Creación de Ingredientes (CRUD: Create)
# =================================================================

# Vista principal para crear un nuevo ingrediente (maneja formulario GET/POST)
def create_ingredient(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    form = None
    if request.method == "POST":
        form = IngredientModelForm(request.POST, request.FILES)
        
        ingredient_create = create_ingredient_model(form)
        if(ingredient_create):
            messages.success(request, 'Se ha creado el ingrediente correctamente.')
            return redirect('list_ingredient')
    else:
        form = IngredientModelForm()
    return render(request, 'ingredient/create_ingredient_bootstrap.html',{"form": form})

# Función auxiliar para guardar un nuevo ingrediente en la base de datos
def create_ingredient_model(form):
    ingredient_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            ingredient_create = True
        except Exception as error:
            print(error)
            pass
    return ingredient_create

# ===================================================================================
# Vista para actualizar/editar un ingrediente existente (carga instancia para editar)
# ===================================================================================
def ingredient_update(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)

    
    if request.method == "POST":
    
        form = IngredientModelForm(request.POST,request.FILES, instance=ingredient)
    
        if (request.method == "POST"):
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Se ha editado el ingrediente correctamente")
                    return redirect('list_ingredient')
                except Exception as error:
                    print(error)
    else:
        form = IngredientModelForm(instance=ingredient)
    return render(request, 'ingredient/updateIngredient.html',{'form': form,'ingredient':ingredient})

# =================================================================
# Vistas de Eliminación de Ingredientes (CRUD: Delete)
# =================================================================
def ingredient_delete(request,ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    try:
        ingredient.delete()
        messages.success(request, "Se ha elimnado el ingrediente correctamente")
    except:
        pass
    return redirect('list_ingredient')

# =================================================================
# Vistas de Creación de Utensilios (CRUD: Create)
# =================================================================

def create_utensil(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    formData = None
    if request.method == "POST":
        formData = request.POST
        
    form = UtensilModelForm(formData)
    
    if (request.method == "POST"):
        
        utensil_create = create_utensil_model(form)
        if(utensil_create):
            messages.success(request, 'Se ha creado el utensilio correctamente.')
            return redirect('list_utensil')
    return render(request, 'utensil/create_utensil_bootstrap.html',{"form": form})

# Función auxiliar para guardar un nuevo ingrediente en la base de datos
def create_utensil_model(form):
    utensil_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            utensil_create = True
        except Exception as error:
            print(error)
            pass
    return utensil_create

# ===================================================================================
# Vista para actualizar/editar un utensilio existente (carga instancia para editar)
# ===================================================================================
def utensil_update(request, utensil_id):
    utensil = Utensil.objects.get(id=utensil_id)
    
    datesForm = None
    
    if request.method == "POST":
        datesForm = request.POST
    
    form = UtensilModelForm(datesForm,instance=utensil)
    
    if (request.method == "POST"):
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se ha editado el utensilio correctamente")
                return redirect('list_utensil')
            except Exception as error:
                print(error)
    return render(request, 'utensil/updateUtensil.html',{'form': form,'utensil':utensil})

# =================================================================
# Vistas de Eliminación de Utensilios (CRUD: Delete)
# =================================================================
def utensil_delete(request,utensil_id):
    utensil = Utensil.objects.get(id=utensil_id)
    try:
        utensil.delete()
        messages.success(request, "Se ha elimnado el utensilio correctamente")
    except:
        pass
    return redirect('list_utensil')
 
 
 
# =================================================================
# Vistas de Creación de Categoria (CRUD: Create)
# =================================================================

# Vista principal para crear una nueva categoria (maneja formulario GET/POST)
def create_category(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    formData = None
    if request.method == "POST":
        formData = request.POST
        
    form = CategoryModelForm(formData)
    
    if (request.method == "POST"):
        
        category_create = create_category_model(form)
        if(category_create):
            messages.success(request, 'Se ha creado la categoria correctamente.')
            return redirect('list_category')
    return render(request, 'category/create_category_bootstrap.html',{"form": form})

# Función auxiliar para guardar un nuevo ingrediente en la base de datos
def create_category_model(form):
    category_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            category_create = True
        except Exception as error:
            print(error)
            pass
    return category_create

# ===================================================================================
# Vista para actualizar/editar una categoria existente (carga instancia para editar)
# ===================================================================================
def category_update(request, category_id):
    category = Category.objects.get(id=category_id)
    
    datesForm = None
    
    if request.method == "POST":
        datesForm = request.POST
    
    form = CategoryModelForm(datesForm, instance=category)
    
    if (request.method == "POST"):
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se ha editado la categoria correctamente")
                return redirect('list_category')
            except Exception as error:
                print(error)
    return render(request, 'category/updateCategory.html',{'form': form,'category':category})

# =================================================================
# Vistas de Eliminación de Categorias (CRUD: Delete)
# =================================================================
def category_delete(request,category_id):
    category = Category.objects.get(id=category_id)
    try:
        category.delete()
        messages.success(request, "Se ha elimnado el category correctamente")
    except:
        pass
    return redirect('list_category')
 
# =================================================================
# Vistas de Creación de Etiquetas (CRUD: Create)
# =================================================================

# Vista principal para crear una nueva etiqueta (maneja formulario GET/POST)
def create_tag(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    formData = None
    if request.method == "POST":
        formData = request.POST
        
    form = TagModelForm(formData)
    
    if (request.method == "POST"):
        
        tag_create = create_tag_model(form)
        if(tag_create):
            messages.success(request, 'Se ha creado la etiqueta correctamente.')
            return redirect('list_tag')
    return render(request, 'tag/create_tag_bootstrap.html',{"form": form})

# Función auxiliar para guardar una nueva etiqueta en la base de datos
def create_tag_model(form):
    tag_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            tag_create = True
        except Exception as error:
            print(error)
            pass
    return tag_create
 
# ===================================================================================
# Vista para actualizar/editar una categoria existente (carga instancia para editar)
# ===================================================================================
def tag_update(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    
    datesForm = None
    
    if request.method == "POST":
        datesForm = request.POST
    
    form = TagModelForm(datesForm, instance=tag)
    
    if (request.method == "POST"):
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se ha editado la etiqueta correctamente")
                return redirect('list_tag')
            except Exception as error:
                print(error)
    return render(request, 'tag/updateTag.html',{'form': form,'tag':tag})

# =================================================================
# Vistas de Eliminación de etiquetas (CRUD: Delete)
# =================================================================
def tag_delete(request,tag_id):
    tag = Tag.objects.get(id=tag_id)
    try:
        tag.delete()
        messages.success(request, "Se ha elimnado la etiqueta correctamente")
    except:
        pass
    return redirect('list_tag')
 
 
 
 
 # =================================================================
# Vistas de Creación de Usuarios (CRUD: Create)
# =================================================================

# Vista principal para crear un nuevo usuario (maneja formulario GET/POST)
def create_user(request):
    
    # Si la peticion es GET se creará el formulario vacío
    # Si la peticioón es POST se creará el formulario con Datos
    formData = None
    if request.method == "POST":
        formData = request.POST
        
    form = UserModelForm(formData)
    
    if (request.method == "POST"):
        
        user_create = create_user_model(form)
        if(user_create):
            messages.success(request, 'Se ha creado el usuario correctamente.')
            return redirect('list_user')
    return render(request, 'user/create_user_bootstrap.html',{"form": form})

# Función auxiliar para guardar una nueva etiqueta en la base de datos
def create_user_model(form):
    user_create = False
    # Se comprueba que el formulario es válido
    if form.is_valid():
        try:
            #Se guarda en la bbdd
            form.save()
            user_create = True
        except Exception as error:
            print(error)
            pass
    return user_create
 
 
 # ===================================================================================
# Vista para actualizar/editar un usuario existente (carga instancia para editar)
# ===================================================================================
def user_update(request, user_id):
    user = User.objects.get(id=user_id)
    
    datesForm = None
    
    if request.method == "POST":
        datesForm = request.POST
    
    form = UserModelForm(datesForm, instance=user)
    
    if (request.method == "POST"):
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se ha editado el usuario correctamente")
                return redirect('list_user')
            except Exception as error:
                print(error)
    return render(request, 'user/updateUser.html',{'form': form,'user':user})

# =================================================================
# Vistas de Eliminación de usuario (CRUD: Delete)
# =================================================================
def user_delete(request,user_id):
    user = User.objects.get(id=user_id)
    try:
        user.delete()
        messages.success(request, "Se ha elimnado el usuario correctamente")
    except:
        pass
    return redirect('list_user')

 
# ******************************************************************
# Vistas de Búsquedas Avanzadas
# ******************************************************************


# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de recetas
# =================================================================
def advance_search_recipe(request):
    form = advanceSearchRecipe(request.GET)
    if(len(request.GET)>0):
        if form.is_valid():
            QSrecipes = Recipe.objects.all()
            search_text = "Filtros:\n"
    
            
            searchText = form.cleaned_data.get('searchText')
            dateSince = form.cleaned_data.get('dateSince')
            dateUntil = form.cleaned_data.get('dateUntil')

            if(searchText != ""):
                QSrecipes = QSrecipes.filter(Q(title__contains=searchText) | Q(description__contains=searchText))
                search_text +=" Nombre o contenido que tenga la palabra: "+searchText+"\n"
            
            if(not dateSince is None):
                  search_text+=" La fecha sea mayor a "+datetime.strftime(dateSince,'%d-%m-%Y')+"\n"
                  QSrecipes = QSrecipes.filter(created__gte=dateSince)

            if(not dateUntil is None):
                search_text +=" La fecha sea menor a "+datetime.strftime(dateUntil,'%d-%m-%Y')+"\n"
                QSrecipes = QSrecipes.filter(created__lte=dateUntil)  
            
            recipes = QSrecipes.all()
            
            return render(request, 'recipe/search_list.html',{"recipe":recipes,"search_text":search_text})         
        else:
            recipes = QSrecipes.all()
    else:
        QSrecipes = Recipe.objects.all()
        recipes = QSrecipes.all()
        form = advanceSearchRecipe(None)
    return render(request, 'recipe/search_form.html',{"form":form})


# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de ingredientes
# =================================================================
def advance_search_ingredient(request):
    form = advanceSearchIngredient(request.GET)
    if(len(request.GET)>0):
        QSingredient = Ingredient.objects.all()
        if form.is_valid():
            text = "Filtros:\n"
    
            
            searchText = form.cleaned_data.get('searchText')
            caloriesMin = form.cleaned_data.get('caloriesMin')
            caloriesMax = form.cleaned_data.get('caloriesMax')
            gluten_free = form.cleaned_data.get('gluten_free')
            is_vegan = form.cleaned_data.get('is_vegan')

            if(searchText != ""):
                QSingredient = QSingredient.filter(name__contains=searchText)
                text +=" Ingredientes que tenga la palabra: "+searchText+"\n"
            
            if(not caloriesMin is None):
                  text+=" Las calorias sean mayores a: " + str(caloriesMin)+"\n"
                  QSingredient = QSingredient.filter(calories__gte=caloriesMin)

            if(not caloriesMax is None):
                text +=" Las calorias sean menos que: " + str(caloriesMax) + "\n"
                QSingredient = QSingredient.filter(calories__lte=caloriesMax)  
            
            if(gluten_free):
                text +=" Sin gluten\n"
                QSingredient = QSingredient.filter(gluten_free=True)
            
            if(is_vegan):
                text +=" es vegano\n"
                QSingredient = QSingredient.filter(is_vegan=True)
           
            ingredient = QSingredient.all()
            
            return render(request, 'ingredient/search_list.html',{"ingredient":ingredient,"search_text":text})         
        else:
            ingredient = QSingredient.all()
    else:
        QSingredient = Ingredient.objects.all()
        ingredient = QSingredient.all()
        form = advanceSearchIngredient(None)
    return render(request, 'ingredient/search_form.html',{"form":form})

# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de utensilios
# =================================================================
def advance_search_utensil(request):
    form = advanceSearchUtensil(request.GET)
    if(len(request.GET)>0):
        QSutensil = Utensil.objects.all()
        if form.is_valid():
            text = "Filtros:\n"
    
            
            searchText = form.cleaned_data.get('searchText')
            searchMaterial = form.cleaned_data.get('searchMaterial')
            dishwasher_safe = form.cleaned_data.get('dishwasher_safe')

            if(searchText != ""):
                QSutensil = QSutensil.filter(name__contains=searchText)
                text +=" Utensilios que tenga la palabra: "+searchText+"\n"
            
            if(searchMaterial != ""):
                QSutensil = QSutensil.filter(material__contains=searchMaterial)
                text +=" Material que tenga la palabra: "+searchText+"\n" 
            
            if(dishwasher_safe):
                QSutensil = QSutensil.filter(dishwasher_safe=True)
                text +=" es APTO para el lavavajillas."
            else:
                QSutensil = QSutensil.filter(dishwasher_safe=False)
                text +=" NO es APTO para el lavavajillas."
           
            utensil = QSutensil.all()
            
            return render(request, 'utensil/search_list.html',{"utensil":utensil,"search_text":text})         
        else:
            utensil = QSutensil.all()
    else:
        QSutensil = Utensil.objects.all()
        utensil = QSutensil.all()
        form = advanceSearchUtensil(None)
    return render(request, 'utensil/search_form.html',{"form":form})


# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de categorias
# =================================================================
def advance_search_category(request):
    form = advanceSearchCategory(request.GET)
    if(len(request.GET)>0):
        QScategory = Category.objects.all()
        if form.is_valid():
            text = "Filtros:\n"
    
            
            searchText = form.cleaned_data.get('searchText')
            description = form.cleaned_data.get('description')
            country = form.cleaned_data.get('country')

            if(searchText != ""):
                QScategory = QScategory.filter(name__contains=searchText)
                text +=" Categorias que tenga la palabra: "+searchText+"\n"
            
            if(description != ""):
                QScategory = QScategory.filter(description__contains=description)
                text +=" Descripcion que tenga la palabra: "+description+"\n"
            
            if(country != ""):
                QScategory = QScategory.filter(country__contains=country)
                text +=" Paises que tengan la palabra: "+country+"\n"
           
            category = QScategory.all()
            
            return render(request, 'category/search_list.html',{"category":category,"search_text":text})      
        else:
            category = QScategory.all()
    else:
        QScategory = Category.objects.all()
        category = QScategory.all()
        form = advanceSearchCategory(None)
    return render(request, 'category/search_form.html',{"form":form})


# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de etiqueta
# =================================================================
def advance_search_tag(request):
    form = advanceSearchTag(request.GET)
    if(len(request.GET)>0):
        QStag = Tag.objects.all()
        if form.is_valid():
            text = "Filtros:\n"
    
            
            searchText = form.cleaned_data.get('searchText')
            description = form.cleaned_data.get('description')
            color = form.cleaned_data.get('color')

            if(searchText != ""):
                QStag = QStag.filter(name__contains=searchText)
                text +=" Etiquetas que tenga la palabra: "+searchText+"\n"
            
            if(color != ""):
                QStag = QStag.filter(color__contains=color)
                text +=" Color que tenga la palabra: "+color+"\n"
            
            if(description != ""):
                QStag = QStag.filter(description__contains=description)
                text +=" Descripcion que tenga la palabra: "+description+"\n"
           
            tag = QStag.all()
            
            return render(request, 'tag/search_list.html',{"tag":tag,"search_text":text})      
        else:
            tag = QStag.all()
    else:
        QStag = Tag.objects.all()
        tag = QStag.all()
        form = advanceSearchTag(None)
    return render(request, 'tag/search_form.html',{"form":form})


# =================================================================
# Vista para realizar búsquedas avanzadas y filtrado de usuario
# =================================================================
def advance_search_user(request):
    form = advanceSearchUser(request.GET)
    if(len(request.GET)>0):
        QSuser = User.objects.all()
        if form.is_valid():
            text = "Filtros:\n"
    
            searchUserName = form.cleaned_data.get('searchUserName')
            searchName = form.cleaned_data.get('searchName')
            dateSince = form.cleaned_data.get('dateSince')
            dateUntil = form.cleaned_data.get('dateUntil')
            description = form.cleaned_data.get('description')
            
            if(searchUserName != ""):
                QSuser = QSuser.filter(username__contains=searchUserName)
                text +=" Usuarios que tenga la palabra en el username: "+searchUserName+"\n"
            if(searchName != ""):
                QSuser = QSuser.filter(name__contains=searchName)
                text +=" Usuarios que tenga la palabra en el nombre o apellido: "+searchName+"\n"
            if(not dateSince is None):
                  text+=" La fecha de creacion sea mayor a "+datetime.strftime(dateSince,'%d-%m-%Y')+"\n"
                  QSuser = QSuser.filter(date_joined__gte=dateSince)
            if(not dateUntil is None):
                text +=" La fecha de creacion sea menor a "+datetime.strftime(dateUntil,'%d-%m-%Y')+"\n"
                QSuser = QSuser.filter(date_joined__lte=dateUntil)
            if(description != ""):
                QSuser = QSuser.filter(description__contains=description)
                text +=" Usuarios que tenga la palabra en la descripcion: "+description+"\n"
            user = QSuser.all()
            return render(request, 'user/search_list.html',{"user":user,"search_text":text})
        else:
            user = QSuser.all()
    else:
        QSuser = User.objects.all()
        user = QSuser.all()
        form = advanceSearchUser(None)
    return render(request, 'user/search_form.html',{"form":form})

# =================================================================
# Vista para realizar listas de los modelos
# =================================================================

# Devuelve todas las recetas con categorias.
def list_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/list.html',{"recipes_list":recipes})
"""SELECT r.*, u.*, ri.*, i.*, c.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
LEFT JOIN recetas_recipe_category rc ON rc.recipe_id = r.id
LEFT JOIN recetas_category c ON rc.category_id = c.id;"""

#Devuelve todos los ingredientes
def list_ingredient(request):
    ingredient = Ingredient.objects.all()
    return render(request, 'ingredient/list.html',{"ingredient_list":ingredient})

#Devuelve todos los utensilios
def list_utensil(request):
    utensil = Utensil.objects.all()
    return render(request, 'utensil/list.html',{"utensil_list":utensil})

#Devuelve todas las categorias
def list_category(request):
    category = Category.objects.all()
    return render(request, 'category/list.html',{"category_list":category})

#Devuelve todas las etiquetas
def list_tag(request):
    tag = Tag.objects.all()
    return render(request, 'tag/list.html',{"tag_list":tag})

#Devuelve todos los usuarios
def list_user(request):
    user = User.objects.all()
    return render(request, 'user/list.html',{"user_list":user})

# Devuelve las recetas que se hayan publicado en octubre de 2025
def get_recipe_date(request, year_recipe, month_recipe):
    recipes=Recipe.objects.all()
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
    # Traemos solo los usuarios filtrando correctamente
    user_list = User.objects.filter(
        Q(usersettings__theme=theme) | Q(usersettings__theme="dark")
    ).select_related("usersettings").order_by("date_joined")

    # Renderizamos la plantilla
    return render(request, 'recipe/url3.html', {"user_list": user_list})
"""SELECT u.*, us.*
FROM recetas_user u
LEFT JOIN recetas_usersettings us ON u.id = us.user_id
WHERE us.theme = '{theme}' OR us.theme = 'dark'
ORDER BY u.date_joined ASC;"""

# Devuelve las recetas que en la descripcion de categoria incluya "Servicio"
def get_category_recipe(request, description):
    recipe = Recipe.objects.all()
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
    recipe = Recipe.objects.all()
    recipe = recipe.filter(comment=None)
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
    recipe = Recipe.objects.all()
    recipe = recipe.filter(ingredient__gluten_free=1)
    return render(request, 'recipe/url8.html', {'recipe': recipe})
"""SELECT r.*, ri.*, i.*
FROM recetas_recipe r
LEFT JOIN recetas_recipeingredient ri ON ri.recipe_id = r.id
LEFT JOIN recetas_ingredient i ON ri.ingredient_id = i.id
WHERE i.gluten_free = TRUE;"""

# Devuelve las recetas que en su descripcion contengan el titulo de la misma
def get_recipe_name_description(request):
    recipe = Recipe.objects.all()
    recipe = recipe.filter(description__contains=F("title"))
    return render(request, 'recipe/url9.html',{'recipe': recipe})
"""SELECT r.*, u.*
FROM recetas_recipe r
JOIN recetas_user u ON r.author_id = u.id
WHERE r.description LIKE CONCAT('%', r.title, '%');"""

# Devuelve los utensilios de cada receta y hace una media de todos los utensilios por receta,
# los utensilios maximos en una receta y los minimos.
def get_recipe_utensils(request):
    count_utensils = Recipe.objects.select_related("author").prefetch_related("category", "utensils", "tags", Prefetch('recipe_ingredient')).annotate(num_utensils=Count("utensils"))
                            
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


#def list_recipes(request):
 #   recipes = (Recipe.objects.raw("SELECT * FROM recetas_recipe r JOIN recetas_user u ON r.author_id = u.id"))
  #  return render(request, 'recipe/list.html',{"recipes_list":recipes})