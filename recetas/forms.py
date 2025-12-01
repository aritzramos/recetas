from django.forms import ModelForm
from django import forms
from .models import Recipe, Ingredient

# =================================================================
# Formulario RecipeModelForm (CRUD: Create y Update)
# =================================================================
# Modelo de formulario de receta
class RecipeModelForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'author', 'category', 'utensils', 'tags']
        labels = {
            "title": ('Nombre de la receta'),
            "description": ('Descripción: '),
            "author": ('Usuario: '),
            "category": ('Categoria: '),
            "utensils": ('Utensilios: '),
            "tags": ('Etiquetas: ')
        }
        help_texts = {
            "title": ('Máximo 100 caracteres'),
            "category": ('Mantén pulsado Ctrl para seleccionar varias'),
            "utensils": ('Mantén pulsado Ctrl para seleccionar varios'),
            "tags": ('Mantén pulsado Ctrl para seleccionar varias')
        }
        widgets = {
            
        }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        
        #Comprobar que no exista una receta con ese nombre
        recipeName = Recipe.objects.filter(title=title).first()
        if( not recipeName is None ):
            if(not self.instance is None and recipeName.id == self.instance.id):
                pass
            else:
                self.add_error('title','Ya existe una receta con ese nombre')
            
        if len(description) < 20:
             self.add_error('description','Debes escribir minimo 20 caracteres')
             
        return self.cleaned_data
    
    
# =================================================================
# Formulario advanceSearchRecipe (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchRecipe(forms.Form):
    
    searchText = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 help_text="Minimo 2 caracteres",
                                 max_length=100)
    
    dateSince = forms.DateField(label="Fecha desde: ",
                                required=False,
                                widget=forms.SelectDateWidget(years=range(2020,2026)))
    
    dateUntil = forms.DateField(label="Fecha hasta: ",
                                required=False,
                                widget=forms.SelectDateWidget(years=range(2020,2026)))
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        dateSince = self.cleaned_data.get('dateSince')
        dateUntil = self.cleaned_data.get('dateUntil')
        
        
        if(searchText == ""
           and dateSince is None
           and dateUntil is None):
            self.add_error('searchText', 'Debes introducir un valor')
            self.add_error('dateSince','Debes introducir un valor')
            self.add_error('dateUntil','Debes introducir un valor')
        else:
            if(searchText != "" and len(searchText)<2):
                self.add_error('searchText','Debes introducir minimo 2 caracteres')
                
            if(len(searchText)>100):
                self.add_error('searchText','Debes introducir máximo 100 caracteres')
                
            if(not dateSince is None and not dateUntil is None and dateUntil < dateSince):
                self.add_error('dateSince','La fecha hasta no puede ser menor que la fecha desde.')
                self.add_error('dateUntil','La fecha hasta no puede ser menor que la fecha desde.')
                
        return self.cleaned_data
    
    
# =================================================================
# Formulario IngredientModelForm (CRUD: Create y Update)
# =================================================================

class IngredientModelForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'calories', 'gluten_free', 'is_vegan', 'image']
        labels = {
            "name": ('Nombre del ingrediente'),
            "calories": ('Calorias'),
            "gluten_free": ('Gluten'),
            "is_vegan": ('¿Es vegano?'),
            "image": ('Imagen')
        }
        help_texts = {
            "name": ('Máximo 100 caracteres'),
            "gluten_free": ('Marca si tiene gluten'),
            "is_vegan": ('Marca si es vegano')
        }
        widgets = {}
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        name = self.cleaned_data.get('name')
        calories = self.cleaned_data.get('calories')
        gluten_free = self.cleaned_data.get('gluten_free')
        is_vegan = self.cleaned_data.get('is_vegan')
        
        #Comprobar que no exista una receta con ese nombre
        ingredientName = Ingredient.objects.filter(name=name).first()
        if( not ingredientName is None ):
            if(not self.instance is None and ingredientName.id == self.instance.id):
                pass
            else:
                self.add_error('name','Ya existe un ingrediente con ese nombre')
            
        if len(name) > 100:
             self.add_error('name','Solo puede tener 100 caracteres como máximo')
             
        return self.cleaned_data
    
# =================================================================
# Formulario advanceSearchIngredient (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchIngredient(forms.Form):
    
    searchText = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 max_length=100)
    
    caloriesMin = forms.IntegerField(required=False,
                                     label="Calorias MINIMAS")
    
    caloriesMax = forms.IntegerField(required=False,
                                     label="Calorias MAXIMAS")
    
    gluten_free = forms.BooleanField(required=False,
                                     label="NO coniene gluten")
    
    is_vegan = forms.BooleanField(required=False,
                                  label="ES vegano")
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        caloriesMin = self.cleaned_data.get('caloriesMin')
        caloriesMax = self.cleaned_data.get('caloriesMax')
        gluten_free = self.cleaned_data.get('gluten_free')
        is_vegan = self.cleaned_data.get('is_vegan')
        
        
        
        if(searchText == ""
           and caloriesMin is None
           and caloriesMax is None
           and gluten_free is False
           and is_vegan is False):
            self.add_error('searchText', 'Debes introducir un valor')
            self.add_error('caloriesMin','Debes introducir un valor')
            self.add_error('caloriesMax','Debes introducir un valor')
            self.add_error('gluten_free','Debes marcar la casilla')
            self.add_error('is_vegan','Debes marcar la casilla')
        else:
            if(searchText != "" and len(searchText)<2):
                self.add_error('searchText','Debes introducir minimo 2 caracteres')
            
            if(len(searchText)>100):
                self.add_error('searchText','Debes introducir máximo 100 caracteres')
            
            if(not caloriesMin is None and not caloriesMax is None and caloriesMax < caloriesMin):
                self.add_error('caloriesMin','Las calorias minimas no pueden ser mayores a las maximas.')
                self.add_error('caloriesMax','Las calorias maximas no pueden ser menores a las minimas.')
                
        return self.cleaned_data