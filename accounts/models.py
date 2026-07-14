from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True,unique=True)

    def __str__(self):
        return self.user.username
    
class Note(models.Model):
    session_key = models.CharField(max_length=100 ,null=True , blank=True )