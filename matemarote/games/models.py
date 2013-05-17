from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class GameRevision(models.Model):
    game = models.ForeignKey(Game)
    version = models.IPAddressField()
    creation_date = models.DateTimeField()
    previous_version = models.ForeignKey('self',null=True)

class GameFlowRule(models.Model):
    objects = InheritanceManager()
    
    game_revision = models.ForeignKey(GameRevision)
    
    def lock_game(self,game_flow_status):
        return False
        
class GameFlowNode(models.Model):        
    game_revision = models.ForeignKey(GameRevision)
    skill_level = models.IntegerField()
    #attributes = models.ManyToManyField(GameFlowAttribute)
    #rules = models.ManyToManyField(GameFlowRule)

class GameFlowRule_GameFullDep(GameFlowRule):
    #rule = models.ForeignKey(GameFlowRule)
    previous_nodes = models.ManyToManyField(GameFlowNode)

    def lock_game(self,game_flow_status):
        return True

class GameFlow(models.Model):
    #root_node = models.ForeignKey(GameFlowNode)
    nodes = models.ManyToManyField(GameFlowNode)
    
    def list_games_per_skill(self, game_flow_status):       
        level_map = {}
        for n in self.nodes.all():
            enabled = True
            if game_flow_status is not None:
                rules = GameFlowRule.objects.filter(game_revision=n.game_revision).select_subclasses()
                for r in rules:
                    enabled = enabled and r.lock_game(game_flow_status)
                
            if n.skill_level in level_map:
                level_map[n.skill_level].append((n.game_revision.pk,enabled))
            else:
                level_map[n.skill_level] = [(n.game_revision.pk,enabled)]
        return level_map


class GameFlowStatus(models.Model):
    user = models.OneToOneField(User)
    
    total_time_played = models.FloatField(default=0.0)
    last_play_timestamp = models.DateTimeField(null=True)
    last_play_totaltime = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)    

class GameFlowNodeStatus(models.Model):
    game_flow_status = models.ForeignKey(GameFlowStatus)
    node = models.ForeignKey(GameFlowNode)
    completion = models.FloatField(default=0.0)
    total_time_played = models.FloatField(default=0.0)
    last_play_timestamp = models.DateTimeField(null=True)
    last_play_totaltime = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)
    
        