from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class monitoreo_del_conteo(models.Model):
    id = models.AutoField(primary_key=True)  # Django automáticamente maneja el ID
    nombre = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha = models.DateField()
    descripcion = models.TextField()
    fecha_caducidad=models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.nombre + '- by' + self.user.username
    
    class Meta:
        db_table = 'monitoreo_del_conteo'  # Establece el nombre de la tabla en la base de datos


class login_escritorio(models.Model):
    id = models.AutoField(primary_key=True)  # Django automáticamente maneja el ID 
    id_usuario= models.IntegerField(default=0)
    nombre=models.CharField(max_length=150)
    contrasenia =models.CharField(max_length=128)
    usuario= models.CharField(max_length=150)
    apellidos= models.CharField(max_length=150)

    class Meta:
       db_table = 'login_escritorio' 