from django.urls import path,include
from django.contrib import admin
from notes import views

app_name = "notes"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("AboutUs/", views.AboutUs_view, name="AboutUs"),
    path("ContactUs/", views.ContactUs_view, name="ContactUs"),
    path('profile/',views.profile_view,name='profile'),
    path("create-note/", views.create_note, name="create_note"),
    path("delete-note/<int:note_id>/",views.delete_note,name="delete_note"),
    path("update-note/<int:note_id>/", views.update_note, name="update_note"),
]