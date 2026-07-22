from django.contrib import admin
from django.urls import path,include
from . import views

app_name ='accounts'

urlpatterns = [
path('login',views.login_view,name='login'),
path('logout',views.logout_view,name='logout'),
path('signup',views.signup_view,name='signup'),
path("login/", views.login_page,name="login_page"),
path("verifyEmail/",views.verify_email_view,name='verify_email'),
path("forgot-password/", views.forgot_password_view, name="forgot_password"),
path("verify-reset/", views.verify_reset_password_view, name="verify_reset_password"),
path("new-password/", views.new_password_view, name="new_password"),
]