from django.db import models
from django.

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)


class Room(models.Model):
    host =
    description = models.TextField(null=True)
    
