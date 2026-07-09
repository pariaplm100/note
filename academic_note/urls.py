from django.contrib import admin
from django.urls import path
from notes import views

urlpatterns = [
    path("admin/", admin.site.urls),    
    path("", views.home, name="home"),
    path("login.html/", views.login_page, name="login_user"),
    path("AboutUs.html/",views.AboutUs,name="AboutUs"),
    path("register/", views.register_user, name="register_user"),
    path("home/",views.home ,name="home" ),
]

