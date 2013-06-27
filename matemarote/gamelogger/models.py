from django.db import models
from games.models import GameFlowNode
from django.contrib.auth.models import User

class PlaySession(models.Model):
    user = models.ForeignKey(User)
    game_flow_node = models.ForeignKey(GameFlowNode)
    ip = models.IPAddressField()
    timestamp = models.DateTimeField(auto_now=True)
    
class LogEntry(models.Model):
    session = models.ForeignKey(PlaySession)
    timestamp = models.DateTimeField(auto_now=True)
    log_code = models.CharField(max_length=255)
    order = models.BigIntegerField()
    _data = models.TextField()
    
    def _get_data(self):
        return loads(self._data)
    def _set_data(self, data):
        self._data = dumps(data) 
    data = property(_get_data, _set_data)
    
