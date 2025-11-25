from django import forms
from django.forms import ModelForm
from .models import *

class RecipeModelForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'author', 'category', 'utensils', 'tags']
        labels = {
            "title": ('Nombre de la receta'),
            "description": ('Descripción: '),
            "author": ('Usuario: '),
            "category": ('Categoria: '),
            "ingredient": ('Ingredientes: '),
            "utensils": ('Utensilios: '),
            "tags": ('Etiquetas: ')
        }
        help_text = {
            "title": ('Máximo 100 caracteres'),
            "category": ('Mantén pulsado Ctrl para seleccionar varias'),
            "ingredient": ('Mantén pulsado Ctrl para seleccionar varios'),
            "utensils": ('Mantén pulsado Ctrl para seleccionar varios'),
            "tags": ('Mantén pulsado Ctrl para seleccionar varias')
        }
        widgets = {
            
        }
        localized_fields = []