from django.db import models
from pygraph.classes.digraph import digraph
# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
class GameFlow(models.Model):
    xml_graph = models.TextField()