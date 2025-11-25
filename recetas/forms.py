from django import forms
from django.forms import ModelForm
from .models import *


# Modelo de formularios

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
        author = self.cleaned_data.get('author')
        category = self.cleaned_data.get('category')
        utensils = self.cleaned_data.get('utensils')
        tags = self.cleaned_data.get('tags')
        
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
    
    
# Formulario generico para busquedas    

class RecipeForm(forms.Form):
    
    title = forms.CharField(label="Titulo",
                            required=True,
                            max_length=200,
                            help_text="200 caracteres como máximo")
    
    description = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea()
                                  )
    
    authorAvalible = User.objects.all()
    author = forms.MultipleChoiceField(
        queryset=authorAvalible,
        widget=forms.Select,
        required=True,
        empty_label="Ninguno"
    )
    
    categoryAvalible = Category.objects.all()
    category = forms.MultipleChoiceField(
        queryset=categoryAvalible,
        widget=forms.Select,
        required=True,
        empty_label="Ninguna"
    )
    
    utensilsAvalible = Utensil.objects.all()
    utensils = forms.MultipleChoiceField(
        queryset=utensilsAvalible,
        widget=forms.Select,
        required=True,
        empty_label="Ninguno"
    )
    
    tagsAvalible = Tag.objects.all()
    Tags = forms.MultipleChoiceField(
        queryset=tagsAvalible,
        widget=forms.Select,
        required=True,
        empty_label="Ninguno"
    )
    
    
class advanceSearchRecipe(forms.Form):
    
    searchText = forms.CharField(required=False)
    
    dateSince = forms.DateField(label="Fecha desde",
                                required=False,
                                widget=forms.SelectDateWidget(years=range(2020,2026)))
    
    dateUntil = forms.DateField(label="Fecha hasta",
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