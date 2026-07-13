from django.contrib import admin
from django.urls import path,include
from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('',include('accounts.urls')),
    path('', include("notes.urls")),
]