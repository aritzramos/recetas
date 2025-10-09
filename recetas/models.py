from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    