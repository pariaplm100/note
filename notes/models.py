from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
class Note(models.Model):
    author = models.ForeignKey( User, on_delete=models.CASCADE, related_name="notes")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="notes")
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
    email = models.EmailField(blank=False)
    message = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True) 
    class Meta:
      ordering = ["create_time"]
      verbose_name="AboutUs Requests"
      verbose_name_plural="AboutUs Requests"
      
    def __str__(self):
        return self.name    
        
class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True) 
    class Meta:
      ordering = ["create_time"]
      verbose_name="ContacUs Forms"
      verbose_name_plural="ContacUs Forms"
      
    def __str__(self):
        return self.full_name  

class NoteFile(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,related_name="files")
    file = models.FileField(upload_to="notes_files/")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-create_time"]  
        
        
    