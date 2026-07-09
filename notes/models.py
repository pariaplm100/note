from django.db import models
from django.contrib.auth.models import User
class notes(models.Model):
    author = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    name = models.CharField(max_length=100)
    topic = models.TextField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)
    class Meta:
      ordering = ["create_time"]
    
    def __str__(self): 
        return f"{self.name}-{self.create_time}"
        
class AboutUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name    