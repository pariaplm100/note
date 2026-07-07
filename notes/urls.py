from django.urls import path
from notes import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_page, name="login_page"),
    path("login/", views.login_user, name="login_user"),
    path("register/", views.register_user, name="register_user"),
    path("home/", views.home_view , name="home"),
    path("",views.home ,name="home" ),
]
