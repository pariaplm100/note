from django.urls import path,include
from django.contrib import admin
from notes import views

app_name = "notes"

urlpatterns = [
    path("", views.home, name="home"),
    path('home/',views.home,name='home'),
    path("AboutUs/", views.AboutUs_view, name="AboutUs"),
    path("ContactUs/", views.ContactUs_view, name="ContactUs"),
    path('profile/',views.profile_view,name='profile'),
]