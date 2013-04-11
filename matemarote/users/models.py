from django.db import models

# Create your models here.
class UserProfile(models.Model):
    birthdate = models.DateField("Fecha de nacimiento")
    gender = models.SmallIntegerField("Sexo",choices=[(1,'hombre'),(2,'mujer')])
    handedness = models.SmallIntegerField("Mano mas habil",choices=[(1,'derecha'),(2,'izquierda'),(3,'ambas')])
    siblingnumber = models.PositiveIntegerField("Hermanos en total",default=0);
    siblingorder = models.PositiveIntegerField("Tu orden de hermandad (1 es el mas grande)",default=0);
    avatar = models.ImageField("tu avatar",upload_to='avatares',default='avatares/pepe.gif');
