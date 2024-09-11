from django.db import models

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
    
   







    
  