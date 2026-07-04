from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_page(request):
    return render(request, "login.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "نام کاربری یا رمز اشتباه است")
            return redirect("login_page")
    return redirect("login_page")

def home_view(request):
    return render(request, "home.html")
def home(request):
    return render(request,"home.html")
def home(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("Email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً ثبت شده")
            return redirect("login_page")

        if password1 == password2:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "ثبت‌نام موفق بود")
            return redirect("login_page")
        else:
            messages.error(request, "رمزها یکسان نیستند")
            return redirect("login_page")

    return redirect("login_page")
