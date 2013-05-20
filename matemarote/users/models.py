from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from games.models import GameFlow,GameFlowStatus

class Program(models.Model):
    game_flow = models.ForeignKey(GameFlow)
    
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField(_("Birth date"))
    gender = models.SmallIntegerField(_("Sex"),choices=[(1,_("Male")),(2,_("Fermale"))])
    handedness = models.SmallIntegerField(_("Handedness"),choices=[(1,_("Right")),(2,_("Left")),(3,_("Both"))])
    siblingnumber = models.PositiveIntegerField(_("Sibling number"),default=0);
    siblingorder = models.PositiveIntegerField(_("Sibling order (1 being the oldest)"),default=0);
    avatar = models.ImageField(_("Avatar"),upload_to='avatares',null=True);
    
    program = models.ForeignKey(Program)
    game_flow_status = models.ForeignKey(GameFlowStatus)

    