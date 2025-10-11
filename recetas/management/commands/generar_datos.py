from django.core.management.base import BaseCommand
from faker import Faker
from recetas.models import *
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generando datos usando Faker'
    
    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        for _ in range(10):
            User.objects.create(
                username = fake.user_name(),
                name = fake.name(),
                password = fake.password(length=10),
                date_joined = fake.date_this_decade(),
                bio = fake.text()
            )
            
        users = list(User.objects.all())
        categories = list(Category.objects.all())
        utensils = list(Utensil.objects.all())
        tags = list(Tag.objects.all())

        for _ in range(10):
            recipe = Recipe.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.paragraph(nb_sentences=3),
                author=random.choice(users),
            )
            recipe.category.add(*random.sample(categories, random.randint(1, 3)))
            recipe.utensils.add(*random.sample(utensils, random.randint(1, 3)))
            recipe.tags.add(*random.sample(tags, random.randint(1, 3)))

        for _ in range(10):
            Ingredient.objects.create(
                name=fake.word().capitalize(),
                calories=random.randint(50, 500),
                gluten_free=fake.boolean(),
                is_vegan=fake.boolean()
            )
        
        recipes = list(Recipe.objects.all())
        ingredients = list(Ingredient.objects.all())

        for _ in range(20):
            RecipeIngredient.objects.create(
                recipe=random.choice(recipes),
                ingredient=random.choice(ingredients),
                quantity=round(random.uniform(0.5, 3.0), 2),
                unit=random.choice(["g", "kg", "ml", "cda", "taza"])
            )
        
        materials = ["madera", "acero inoxidable", "plástico", "silicona"]
        for _ in range(10):
            Utensil.objects.create(
                name=fake.word().capitalize(),
                material=random.choice(materials),
                dishwasher_safe=fake.boolean()
            )
        
        for recipe in recipes:
            for i in range(random.randint(2, 5)):
                Step.objects.create(
                    recipe=recipe,
                    order=i + 1,
                    instruction=fake.sentence(nb_words=10),
                    estimated_time=random.randint(1, 10)
                )
        
        for _ in range(10):
            Category.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=100),
                is_visible=fake.boolean()
            )
            
        for _ in range(15):
            Comment.objects.create(
                recipe=random.choice(recipes),
                author=random.choice(users),
                content=fake.paragraph(nb_sentences=2)
            )
        
        colors = ["red", "green", "blue", "orange", "purple"]  
        for _ in range(10):
            Tag.objects.create(
                name=fake.word().capitalize(),
                color=random.choice(colors),
                description=fake.text(max_nb_chars=100),
                popularity=random.randint(0, 100)
            )
        
        for _ in range(15):
            Rating.objects.create(
                recipe=random.choice(recipes),
                user=random.choice(users),
                stars=random.randint(1, 5),
                comment=fake.sentence(),
            )
            
        for _ in range(10):
            ContactMessage.objects.create(
                name=fake.name(),
                email=fake.email(),
                subject=fake.sentence(nb_words=5),
                message=fake.text(max_nb_chars=150)
            )
            
        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))
        