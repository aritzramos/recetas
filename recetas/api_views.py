from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def recipe_list_api(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def recipe_list_api_mejorado(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializerMejorado(recipes, many=True)
    return Response(serializer.data)