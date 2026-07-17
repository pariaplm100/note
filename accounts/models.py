from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone_number = models.CharField(max_length=20, blank=True,unique=True)
    
    image = models.ImageField(upload_to="profile_images/",default="profile_images/default.png")
    
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username