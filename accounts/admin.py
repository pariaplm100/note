from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    search_fields = ("user__username", "phone_number")

admin.site.register(Profile,ProfileAdmin)