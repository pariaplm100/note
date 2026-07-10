from django.urls import path,include
from django.contrib import admin
from notes import views
from django.contrib.auth import views as auth_views

app_name = "notes"

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    path("", views.home, name="home"),

    path("login/", views.login_page, name="login_page"),
    
    path("login_user/", views.login_user, name="login_user"),
    
    path("register/", views.register_user, name="register_user"),

    path("AboutUs/", views.AboutUs_view, name="AboutUs"),

    path('contact-us/', views.ContactUs_view, name='ContactUs'),

]