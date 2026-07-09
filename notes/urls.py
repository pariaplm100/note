from django.urls import path
from notes import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login_user"),
    path("AboutUs.html/",views.AboutUs,name="AboutUs"),
    path("register/", views.register_user, name="register_user"),
    path("home/", views.home_view , name="home"),
    path("home/",views.home ,name="home" ),
]
