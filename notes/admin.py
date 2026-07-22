from django.contrib import admin
from notes.models import Note,AboutUs,ContactUs

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = "create_time"

    list_display = (
        'id',
        'author_username',
        'name',
        'status',
        'create_time',
        'update_time'
    )

    search_fields = ['status', 'name', 'author__username']
    list_filter = ('status','author')
    ordering = ['create_time']

    def author_username(self, obj):
        return obj.author.username if obj.author else "-"
    
    author_username.short_description = "Author"
    
class AboutUsAdmin(admin.ModelAdmin):
    date_hierarchy = "create_time"
    list_display = (
        'id','name','email','message','create_time','update_time'
        )
    search_fields =['email','name']
    ordering = ['create_time']
    
class ContactUsAdmin(admin.ModelAdmin):
    date_hierarchy = "create_time"
    list_display = (
        'id','full_name','email','message','create_time','update_time'
        )
    
    search_fields =['email','full_name']
    ordering = ['create_time']
    
admin.site.register(Note,NoteAdmin) 
admin.site.register(AboutUs,AboutUsAdmin)
admin.site.register(ContactUs,ContactUsAdmin)