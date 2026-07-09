from django.urls import path,include
from notes import views


urlpatterns = [
    path("", views.home, name="home"),

    path("login/", views.login_page, name="login_page"),
    path("login_user/", views.login_user, name="login_user"),

    path("register/", views.register_user, name="register_user"),

    path("AboutUs.html/", views.AboutUs_view, name="AboutUs"),

    path("captcha/", include("captcha.urls")),
]