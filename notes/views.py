from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .captcha import Captcha

def login_page(request):
    login_captcha = str(Captcha())
    register_captcha = str(Captcha())

    request.session["login_captcha"] = login_captcha
    request.session["register_captcha"] = register_captcha

    return render(request, "login.html", {
        "captcha1": login_captcha,
        "captcha2": register_captcha,
    })
    

def login_user(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user_captcha = request.POST.get("captcha")


        real_captcha = request.session.get("login_captcha")


        if user_captcha != real_captcha:
            request.session.pop("login_captcha", None)
            messages.error(request, "Captcha is incorrect.")
            return redirect("login_page")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            request.session.pop("login_captcha", None)

            return redirect("home")

        else:
            request.session.pop("login_captcha", None)
            messages.error(request, "Username or password is incorrect.")
            return redirect("login_page")
    return redirect("login_page")
    

def home(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def register_user(request):

    if request.method == "POST":

        user_captcha = request.POST.get("captcha")
        real_captcha = request.session.get("register_captcha")

        if user_captcha != real_captcha:
            request.session.pop("register_captcha", None)
            messages.error(request, "Captcha is incorrect.")
            return redirect("login_page")

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            request.session.pop("register_captcha", None)
            messages.error(request, "این نام کاربری قبلاً ثبت شده")
            return redirect("login_page")

        if password1 == password2:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            request.session.pop("register_captcha", None)
            messages.success(request, "ثبت‌نام موفق بود")
            return redirect("login_page")

        else:
            request.session.pop("register_captcha", None)
            messages.error(request, "رمزها یکسان نیستند")
            return redirect("login_page")

    return redirect("login_page")