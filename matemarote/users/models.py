from django.utils.translation import ugettext as _
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    birthdate = models.DateField(_("Birth date"))
    gender = models.SmallIntegerField(_("Sex"),choices=[(1,_("Male")),(2,_("Fermale"))])
    handedness = models.SmallIntegerField(_("Handedness"),choices=[(1,_("Right")),(2,_("Left")),(3,_("Both"))])
    siblingnumber = models.PositiveIntegerField(_("Sibling number"),default=0);
    siblingorder = models.PositiveIntegerField(_("Sibling order (1 being the oldest)"),default=0);
    avatar = models.ImageField(_("Avatar"),upload_to='avatares',default='avatares/pepe.gif');

	program = models.ForeignKey('Program')

class Program(models.Model):
	name = models.CharField(max_length=150)
	language = models.SmallIntegerField(_("Language"),choices=[(1,_("Spanish")),(2,_("English"))])
	
	parent = models.ForeignKey('self', null=True)
	gameflow = models.ForeignKey('GameFlow', null=True)
	
