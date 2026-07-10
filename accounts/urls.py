from django.contrib import admin
from django.urls import path,include
from . import views

app_name ='accounts'

urlpatterns = [
path('login',views.login_view,name='login'),
path('logout',views.logout_view,name='logout'),
path('signup',views.signup_view,name='signup'),
path("login/", views.login_page,name="login_page"),
path("passwordreset/",views.password_reset_view,name='password_reset'),
]