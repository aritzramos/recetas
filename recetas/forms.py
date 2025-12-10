from django.forms import ModelForm
from django import forms
from .models import UsuarioRol, Recipe, Ingredient, Utensil, Category, Tag, User
from django.contrib.auth.forms import UserCreationForm



# =================================================================
# Formulario RegistroFormUsuario (CRUD: Create)
# =================================================================

class RegistroFormUsuario(UserCreationForm):

    name = forms.CharField(label="Nombre Completo", required=True)
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = UsuarioRol

        fields = ('username', 'name', 'email', 'password1', 'password2')


# =================================================================
# Formulario RegistroFormModerador (CRUD: Create)
# =================================================================

class RegistroFormModerador(UserCreationForm):
    
    bio = forms.CharField(widget=forms.Textarea, label="Biografía", required=True)
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = UsuarioRol
        fields = ('username', 'email', 'bio', 'password1', 'password2')

# =================================================================
# Formulario RecipeModelForm (CRUD: Create y Update)
# =================================================================
# Modelo de formulario de receta
class RecipeModelForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'utensils', 'tags']
        labels = {
            "title": ('Nombre de la receta'),
            "description": ('Descripción: '),
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
            "description": forms.Textarea(), 
            "category": forms.SelectMultiple(),
            "utensils": forms.SelectMultiple(),
            "tags": forms.SelectMultiple(),
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
    
    userSession = forms.BooleanField(required=False,
                                     label="Solo mis recetas")
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        dateSince = self.cleaned_data.get('dateSince')
        dateUntil = self.cleaned_data.get('dateUntil')
        userSession = self.cleaned_data.get('userSession')
        
        
        if(searchText == ""
           and dateSince is None
           and dateUntil is None
           and userSession is False):
            self.add_error('searchText', 'Debes introducir un valor')
            self.add_error('dateSince','Debes introducir un valor')
            self.add_error('dateUntil','Debes introducir un valor')
            self.add_error('userSession','Debes marcar la casilla')
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
            "gluten_free": ('Marca si NO tiene gluten'),
            "is_vegan": ('Marca si es vegano')
        }
        widgets = {
            "calories": forms.NumberInput(), 
            "image": forms.ClearableFileInput(),
            }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        name = self.cleaned_data.get('name')
        
        #Comprobar que no exista un ingrediente con ese nombre
        if name is not None:
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
    
    
# =================================================================
# Formulario UtensilModelForm (CRUD: Create y Update)
# =================================================================

class UtensilModelForm(ModelForm):
    class Meta:
        model = Utensil
        fields = ['name', 'material', 'dishwasher_safe']
        labels = {
            "name": ('Nombre del utensilio'),
            "material": ('Nombre del material'),
            "dishwasher_safe": ('Apto para lavavajillas')
        }
        help_texts = {
            "name": ('Máximo 50 caracteres'),
            "material": ('Maximo 50 caracteres'),
            "dishwasher_safe": ('Marca si es apto para lavavajillas')
        }
        widgets = {
            "name": forms.TextInput(), 
            "material": forms.TextInput(),
            "dishwasher_safe": forms.CheckboxInput(),
        }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        name = self.cleaned_data.get('name')
        material = self.cleaned_data.get('material')
        
        #Comprobar que no exista un utensilio con ese nombre
        utensilName = Utensil.objects.filter(name=name).first()
        if( not utensilName is None ):
            if(not self.instance is None and utensilName.id == self.instance.id):
                pass
            else:
                self.add_error('name','Ya existe un utensilio con ese nombre')
            
        if len(name) > 50:
             self.add_error('name','Solo puede tener 50 caracteres como máximo')
             
        if len(material) > 50:
             self.add_error('material','Solo puede tener 50 caracteres como máximo')
             
        return self.cleaned_data
    
# =================================================================
# Formulario advanceSearchUtensil (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchUtensil(forms.Form):
    
    searchText = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 max_length=50)
    
    searchMaterial = forms.CharField(required=False,
                                 label="Material",
                                 max_length=50)
    
    dishwasher_safe = forms.BooleanField(required=False,
                                     label="APTO para el lavavajillas")
    
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        searchMaterial = self.cleaned_data.get('searchMaterial')

        
        
        if(searchText != "" and len(searchText)<2):
                self.add_error('searchText','Debes introducir minimo 2 caracteres')
                
        if(searchMaterial != "" and len(searchMaterial)<2):
                self.add_error('searchText','Debes introducir minimo 2 caracteres')
            
        if(len(searchText)>50 or len(searchMaterial)>50):
                self.add_error('searchText','Debes introducir máximo 50 caracteres')
                
        if(len(searchMaterial)>50):
                self.add_error('searchMaterial','Debes introducir máximo 50 caracteres')
                
        return self.cleaned_data
    
    
# =================================================================
# Formulario CategoryModelForm (CRUD: Create y Update)
# =================================================================

class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'country', 'image']
        labels = {
            "name": ('Nombre de la categoria'),
            "description": ('Descripción'),
            "country": ('País de origen'),
            "image": ('Imagen')
        }
        help_texts = {
            "name": ('Máximo 30 caracteres'),
            "description": ('Descripción de la categoria'),
            "country": ('Máximo 30 caracteres')
        }
        widgets = {
            "description": forms.Textarea(attrs={'rows': 3}), 
            "image": forms.ClearableFileInput(),
        }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        name = self.cleaned_data.get('name')
        country = self.cleaned_data.get('country')
        
        #Comprobar que no exista un ingrediente con ese nombre
        categoryName = Category.objects.filter(name=name).first()
        if( not categoryName is None ):
            if(not self.instance is None and categoryName.id == self.instance.id):
                pass
            else:
                self.add_error('name','Ya existe una categoria con ese nombre')
        if name is not None:    
            if len(name) > 30:
                self.add_error('name','Solo puede tener 100 caracteres como máximo')
        if country is not None:
            if len(country) > 30:
                self.add_error('country','Solo puede tener 30 caracteres como máximo')
             
        return self.cleaned_data
    
# =================================================================
# Formulario advanceSearchCategory (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchCategory(forms.Form):
    
    searchText = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 max_length=100)
    
    description = forms.CharField(required=False,
                                     label="Descripción",
                                     max_length=200)
    country = forms.CharField(required=False,
                                     label="País",
                                     max_length=30)
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        description = self.cleaned_data.get('description')
        country = self.cleaned_data.get('country')
        
        
        if(searchText == ""
           and description == ""
           and country == ""):
            self.add_error('searchText', 'Debes introducir un valor')
            self.add_error('description','Debes introducir un valor')
            self.add_error('country','Debes introducir un valor')
        else:
            
            if(len(searchText)>100):
                self.add_error('searchText','Debes introducir máximo 100 caracteres')
            
            if(len(description)>200):
                self.add_error('description','Debes introducir máximo 200 caracteres')
            
            if(len(country)>30):
                self.add_error('country','Debes introducir máximo 30 caracteres')
                
        return self.cleaned_data
    
    
# =================================================================
# Formulario TagModelForm (CRUD: Create y Update)
# =================================================================

class TagModelForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color', 'description']
        labels = {
            "name": ('Nombre de la categoria'),
            "color": ('Color'),
            "description": ('Descripción')
        }
        help_texts = {
            "name": ('Máximo 30 caracteres'),
            "color": ('Color de la etiqueta'),
            "description": ('Descripción de la categoria')
        }
        widgets = {
            "color": forms.TextInput(attrs={'type': 'color'}),
            "description": forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe el tipo de receta que identifica esta etiqueta'}),
        }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        name = self.cleaned_data.get('name')
        color = self.cleaned_data.get('color')
        
        #Comprobar que no exista un tag con ese nombre
        tagName = Tag.objects.filter(name=name).first()
        if( not tagName is None ):
            if(not self.instance is None and tagName.id == self.instance.id):
                pass
            else:
                self.add_error('name','Ya existe una etiqueta con ese nombre')
        if name is not None:    
            if len(name) > 30:
                self.add_error('name','Solo puede tener 30 caracteres como máximo')
            if name and name.strip():
                if ' ' in name:
                    self.add_error('name','El nombre no puede contener espacios')

        if color is not None:
            if len(color) > 20:
                self.add_error('color','Solo puede tener 20 caracteres como máximo')
             
        return self.cleaned_data
    
# =================================================================
# Formulario advanceSearchTag (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchTag(forms.Form):
    
    searchText = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 max_length=30)
    
    color = forms.CharField(required=False,
                                     label="Color",
                                     max_length=20)
    description = forms.CharField(required=False,
                                     label="Descripción",
                                     max_length=200)
    
    def clean(self):
        
        super().clean()
        
        searchText = self.cleaned_data.get('searchText')
        description = self.cleaned_data.get('description')
        color = self.cleaned_data.get('color')
        
        
        if(searchText == ""
           and description == ""
           and color == ""):
            self.add_error('searchText', 'Debes introducir un valor')
            self.add_error('description','Debes introducir un valor')
            self.add_error('color','Debes introducir un valor')
        else:
            
            if(len(searchText)>30):
                self.add_error('searchText','Debes introducir máximo 30 caracteres')
            
            if searchText and searchText.strip():
                if ' ' in searchText:
                    self.add_error('searchText','El nombre no puede contener espacios')
            
            if(len(color)>20):
                self.add_error('color','Debes introducir máximo 20 caracteres')
            
            if(len(description)>200):
                self.add_error('description','Debes introducir máximo 200 caracteres')
              
        return self.cleaned_data
    
    
    # =================================================================
# Formulario UserModelForm (CRUD: Create y Update)
# =================================================================

class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['usuarioRol', 'name', 'bio']
        labels = {
            "usuarioRol": ('Nombre de usuario'),
            "name": ('Nombre completo'),
            "bio": ('Biografía')
        }
        help_texts = {
            "usuarioRol": ('Máximo 15 caracteres'),
            "name": ('Máximo 50 caracteres'),
            "bio": ('Escribe una breve biografía')
        }
        widgets = {
            "bio": forms.Textarea(attrs={'rows': 4})
        }
        localized_fields = []
        
    def clean(self):
        #Con esto validamos con el modelo actual.
        super().clean()
        
        #Pasamos los datos
        usuarioRol = self.cleaned_data.get('usuarioRol')
        name = self.cleaned_data.get('name')
        
        #Comprobar que no exista un usuario con ese nick
        userName = User.objects.filter(username=usuarioRol).first()
        if( not userName is None ):
            if(not self.instance is None and userName.id == self.instance.id):
                pass
            else:
                self.add_error('username','Ya existe un usuario con ese nombre')
        if usuarioRol is not None:    
            if len(usuarioRol) > 15:
                self.add_error('username','Solo puede tener 15 caracteres como máximo')
            if usuarioRol and usuarioRol.strip():
                if ' ' in usuarioRol:
                    self.add_error('username','El nombre de usuario no puede contener espacios')
        if name is not None:
            if len(name) > 50:
                self.add_error('name','Solo puede tener 50 caracteres como máximo')
        
        
             
        return self.cleaned_data
    
    

# =================================================================
# Formulario advanceSearchUser (CRUD: Read - Búsqueda Avanzada)
# =================================================================
    
class advanceSearchUser(forms.Form):
    
    searchUsername = forms.CharField(required=False,
                                 label="Texto de búsqueda",
                                 max_length=15)
    
    searchName = forms.CharField(required=False,
                                 label="Nombre completo",
                                 max_length=50)
    
    dateSince = forms.DateField(label="Fecha desde: ",
                                required=False,
                                widget=forms.SelectDateWidget(years=range(2020,2026)))
    
    dateUntil = forms.DateField(label="Fecha hasta: ",
                                required=False,
                                widget=forms.SelectDateWidget(years=range(2020,2026)))
    
    description = forms.CharField(required=False,
                                     label="Descripción",
                                     max_length=200)
    
    def clean(self):
        
        super().clean()
        
        searchUsername = self.cleaned_data.get('searchUsername')
        searchName = self.cleaned_data.get('searchName')
        dateSince = self.cleaned_data.get('dateSince')
        dateUntil = self.cleaned_data.get('dateUntil')
        description = self.cleaned_data.get('description')
        
        
        if(not searchUsername
           and not searchName
           and dateSince is None
           and dateUntil is None
           and not description):
            self.add_error('searchUsername', 'Debes introducir un valor')
            self.add_error('searchName','Debes introducir un valor')
            self.add_error('dateSince','Debes introducir un valor')
            self.add_error('dateUntil','Debes introducir un valor')
            self.add_error('description','Debes introducir un valor')
        else:
            
            if(searchUsername is not None and len(searchUsername)>15):
                self.add_error('searchUsername','Debes introducir máximo 15 caracteres')
            
            if searchUsername and searchUsername.strip():
                if ' ' in searchUsername:
                    self.add_error('searchUsername','El nombre de usuario no puede contener espacios')
            
            if(len(searchName)>50):
                self.add_error('searchName','Debes introducir máximo 50 caracteres')
            
            if(not dateSince is None and not dateUntil is None and dateUntil < dateSince):
                self.add_error('dateSince','La fecha hasta no puede ser menor que la fecha desde.')
                self.add_error('dateUntil','La fecha hasta no puede ser menor que la fecha desde.')
            
            if(len(description)>200):
                self.add_error('description','Debes introducir máximo 200 caracteres')
              
        return self.cleaned_data