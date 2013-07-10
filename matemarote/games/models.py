from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from django.forms import ModelForm, Textarea
from django.core.exceptions import ObjectDoesNotExist

class Game(models.Model):
    name = models.SlugField(unique=True,null=False,blank=False)
    description = models.TextField()
    
    def __str__(self): return self.name
    #def getGameRevisions(self):
    #        return GameRevision.objects.filter(game = self)
    
    #game_revisions = property(getGameRevisions)
    class Meta:
        permissions = (
            ('game_admin', 'Game administrator permission'),
        )

    
class GameRevision(models.Model):
    game = models.ForeignKey(Game)
    version = models.IPAddressField()
    creation_date = models.DateTimeField()
    previous_version = models.ForeignKey('self',null=True,blank=True)

    def __str__(self): return self.game.name + ' (' + str(self.version) + ')'
    
class GameFlowRule(models.Model):
    objects = InheritanceManager()
    
    gameflow_node = models.ForeignKey('GameFlowNode')
    
    def lock_game(self,gf_status):
        return False

class GameFlowNode(models.Model):        
    gameflow = models.ForeignKey('GameFlow')
    game_revision = models.ForeignKey(GameRevision)
    skill_level = models.IntegerField()
    
    def is_enabled(self,gameflow_status):
        enabled = True
        rules = GameFlowRule.objects.filter(gameflow_node=self).select_subclasses()
        for r in rules:
            enabled = enabled and not r.lock_game(gameflow_status)
            
        return enabled



class GameFlowRule_GameFullDep(GameFlowRule):
    #rule = models.ForeignKey(GameFlowRule)
    previous_nodes = models.ManyToManyField(GameFlowNode)

    def lock_game(self,gf_status):
        status_nodes = GameFlowNodeStatus.objects.filter(gameflow_status=gf_status)
        lock = False
        for n in self.previous_nodes.all():
            st_node = status_nodes.get(node=n)
            lock = lock or not (st_node.game_finished)
        return lock

class GameFlowRule_GamePartialCompletionDep(GameFlowRule):
    completion_threshold = models.IntegerField()
    previous_nodes = models.ManyToManyField(GameFlowNode)

    def lock_game(self,gf_status):
        status_nodes = GameFlowNodeStatus.objects.filter(gameflow_status=gf_status)
        #print "\n -------------------- ", status_nodes
        lock = False
        for n in self.previous_nodes.all():
            try:
                st_node = status_nodes.get(node=n)
                lock = lock or not (st_node.completion > self.completion_threshold)
            except ObjectDoesNotExist:
                lock = True
    
            #print "\n -------------------- ", st_node.completion, " > ", self.completion_threshold
        return lock

class GameFlow(models.Model):
    
    def list_games_per_skill(self, gameflow_status):       
        level_map = {}
        for n in GameFlowNode.objects.filter(gameflow=self):
            enabled = True
            if gameflow_status is not None:
                enabled = n.is_enabled(gameflow_status)
                
            if n.skill_level in level_map:
                level_map[n.skill_level].append((n,enabled))
            else:
                level_map[n.skill_level] = [(n,enabled)]
        return level_map

class GameFlowStatus(models.Model):
    user = models.OneToOneField(User)
    
    total_time_played = models.FloatField(default=0.0)
    last_play_timestamp = models.DateTimeField(null=True)
    last_play_totaltime = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)    

class GameFlowNodeStatus(models.Model):
    gameflow_status = models.ForeignKey(GameFlowStatus)
    node = models.ForeignKey(GameFlowNode)
    game_finished = models.BooleanField(default=False)
    completion = models.IntegerField(default=0)
    total_time_played = models.FloatField(default=0.0)
    last_play_timestamp = models.DateTimeField(null=True)
    last_play_totaltime = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)
