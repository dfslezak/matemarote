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
    
class GameFlowNode(models.Model):
    def clean(self):
        level_diff = [((self.skill_level - xxx.skill_level) == 1) for xxx in self.previous_level_dep.objects.all()]
        print level_diff
        if False in level_diff:
            raise ValidationError(u'%s is not an even number' % value)
        
    game_revision = models.ForeignKey(GameRevision)
    skill_level = models.IntegerField()
    previous_level_dep = models.ManyToManyField('self')
    
#class GameFlow(models.Model):
    
#    xml_graph = models.TextField()