from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.




class  Create_subs(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
       return self.nickname

   

class CreateUser(AbstractUser):
    edad = models.PositiveIntegerField(null=True)
    nickname = models.CharField(max_length=100,null=True)
    cumpleaños = models.DateTimeField(null=True)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado_cpl = models.CharField(max_length=100)
    modo_de_juego = models.CharField(max_length=100)
    reclutado_por = models.ForeignKey('Create_subs', on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)
    is_sub_leader = models.BooleanField(default=False)
    def is_sub(self):
        return self.reclutado_por is not None  # Si el usuario tiene un reclutador, es un sub

    def __str__(self):
      
        if self.nickname:
            return f"{self.username} - {self.reclutado_por.nickname}"
        return self.username

class Members_eliminated(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveBigIntegerField(default=0)  
    nickname = models.CharField(max_length=100)
    cumpleaños = models.DateTimeField(default=timezone.now) 
    pais = models.CharField(max_length=100, )  
    ciudad = models.CharField(max_length=100, )  
    estado_cpl = models.CharField(max_length=100, )  
    modo_de_juego = models.CharField(max_length=100, )  
    razon = models.TextField()
    reclutado_por = models.ForeignKey(Create_subs, on_delete=models.CASCADE)
    fecha_elimiado = models.DateTimeField()
    is_active = models.BooleanField(default= False)

    def __str__(self):
        return self.nombre + ' by ' + self.reclutado_por.nickname
    
  