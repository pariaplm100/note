from django.contrib import admin
from django.urls import path,include
from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',include('accounts.urls')),
    
    path("", views.home, name="home"),
    
    
    path('', include("notes.urls")),

    path("AboutUs/", views.AboutUs_view, name="AboutUs"),
    
    path("ContactUs/", views.ContactUs_view, name="ContactUs"),

]