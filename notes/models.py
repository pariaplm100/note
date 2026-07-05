from django.db import models

class notes(models.Model):
    name = models.CharField(max_length=100)
    topic = models.TextField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)
    class Meta:
      ordering = ["create_time"]
    
    def __str__(self): 
        return f"{self.name}-{self.create_time}"
    