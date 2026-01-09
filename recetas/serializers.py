from rest_framework import serializers
from .models import *

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'    


class RecipeSerializerMejorado(serializers.ModelSerializer):
    
    author = AuthorSerializer()
    
    category = CategorySerializer(read_only=True, many=True)
    
    created = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        fields = ('title', 'description', 'author', 'category', 'created')
        model = Recipe
    
    