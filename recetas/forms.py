from django.forms import ModelForm
from django import forms
from .models import Recipe 

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
            
            if(not dateSince is None and not dateUntil is None and dateUntil < dateSince):
                self.add_error('dateSince','La fecha hasta no puede ser menor que la fecha desde.')
                self.add_error('dateUntil','La fecha hasta no puede ser menor que la fecha desde.')
                
        return self.cleaned_data