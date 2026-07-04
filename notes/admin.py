from django.contrib import admin
from .models import Notes

# Register your models here.

class userAdmin(admin.ModelAdmin): 
    date_hierarchy="create_time"
    
admin.site.register(Notes,userAdmin) 