from django.db import models
from django.core.exceptions import ValidationError

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class GameRevision(models.Model):
    game = models.ForeignKey(Game)
    version = models.IPAddressField()
    creation_date = models.DateTimeField()
    previous_version = models.ForeignKey('self',null=True)

class GameFlowAttribute(models.Model):
    class Meta:
        abstract = True

class GameFlowRule(models.Model):
    DEPENDENCY = 1
    
    RULE_TYPE_CHOICES = (
        (DEPENDENCY, 'Dependency'),
        )
    
    rule_type = models.IntegerField(choices=RULE_TYPE_CHOICES)
    class Meta:
        abstract = True

class GameFlowNode(models.Model):        
    game_revision = models.ForeignKey(GameRevision)
    skill_level = models.IntegerField()
    attributes = models.ManyToManyField(GameFlowAttribute)
    rules = models.ManyToManyField(GameFlowRule)
    
class GameFlowRule_GameDep(GameFlowRule):
    rule_type = DEPENDENCY
    previous_nodes = models.ManyToManyField(GameFlowNode)

    
#class GameFlow(models.Model):
    
#    xml_graph = models.TextField()