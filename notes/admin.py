from django.contrib import admin
from .models import notes

# Register your models here.

class NoteAdmin(admin.ModelAdmin): 
    date_hierarchy = "create_time"
    list_display = ('id','name','status','create_time','update_time')
    search_fields = ['status','name']
    ordering = ['create_time']
    
admin.site.register(notes,NoteAdmin) 