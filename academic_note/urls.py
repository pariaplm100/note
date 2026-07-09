from django.contrib import admin
from django.urls import path,include
from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("", views.home, name="home"),

    path("login/", views.login_page, name="login_page"),
    
    path("login_user/", views.login_user, name="login_user"),

    path("register/", views.register_user, name="register_user"),
    
    path("", include("notes.urls")),

    path("AboutUs/", views.AboutUs_view, name="AboutUs"),

]