from django.db import models
from django.utils import timezone

# Create your models here.




class  Create_subs(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
       return self.nickname

   




class Create_members(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    nickname = models.CharField(max_length=100)
    happy_birthday = models.DateTimeField()
    
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    cpl_status = models.CharField(max_length=100)
    mode_play = models.CharField(max_length=100)
    recruited = models.ForeignKey(Create_subs, on_delete=models.CASCADE)
    


    def __str__(self):
        return self.name + '-' + self.nickname 


class Members_eliminated(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)  # Añadir default
    nickname = models.CharField(max_length=100)
    happy_birthday = models.DateTimeField(default=timezone.now)  # Añadir default
    country = models.CharField(max_length=100, default='')  # Añadir default
    city = models.CharField(max_length=100, default='')  # Añadir default
    cpl_status = models.CharField(max_length=100, default='')  # Añadir default
    mode_play = models.CharField(max_length=100, default='')  # Añadir default
    reason = models.TextField()
    recruited = models.ForeignKey(Create_subs, on_delete=models.CASCADE)
    date_eliminate = models.DateTimeField()

    def __str__(self):
        return self.name + ' by ' + self.nickname


    
  