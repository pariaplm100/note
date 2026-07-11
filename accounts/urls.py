from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('login/submit/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('passwordreset/', views.password_reset_view, name='password_reset'),
]