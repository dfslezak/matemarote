from django.utils.translation import ugettext as _
from django.conf.global_settings import LANGUAGES
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from games.models import GameFlow,GameFlowStatus
from django.db.models.signals import post_save
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget

class Program(models.Model):
    game_flow = models.ForeignKey(GameFlow)
    
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField(_("Birth date"),null=True)
    gender = models.SmallIntegerField(_("Sex"),choices=[(1,_("Male")),(2,_("Fermale"))],null=True)
    handedness = models.SmallIntegerField(_("Handedness"),choices=[(1,_("Right")),(2,_("Left")),(3,_("Both"))],null=True)
    siblingnumber = models.PositiveIntegerField(_("Sibling number"),default=0,null=True);
    siblingorder = models.PositiveIntegerField(_("Sibling order (1 being the oldest)"),default=0,null=True);
    avatar = models.ImageField(_("Avatar"),upload_to='avatares',null=True,blank=True);

    program = models.ForeignKey('Program',default=1)
    game_flow_status = models.ForeignKey(GameFlowStatus,null=True)

class Program(models.Model):
    name = models.CharField(max_length=150)
    #language = models.SmallIntegerField(_("Language"),choices=[(1,_("Spanish")),(2,_("English"))])
    language = models.CharField(choices=LANGUAGES)
    parent = models.ForeignKey('self', null=True)
    entry_url = models.CharField(max_length=150)
    
    gameflow = models.ForeignKey('GameFlow', null=True)

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthdate','gender','handedness','siblingnumber','siblingorder','avatar']
        widgets = {'birthdate': AdminDateWidget}

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)