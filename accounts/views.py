from django.shortcuts import render,redirect
from accounts.captcha import Captcha
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user_captcha = request.POST.get("captcha")
        phone_number= request.POST.get("phone_number")


        real_captcha = request.session.get("login_captcha")

        new_captcha = str(Captcha())
        request.session["login_captcha"] = new_captcha

        context = {
        "captcha1" : new_captcha,
        "username": username,
        "username_error" : "",
        "password_error" : "",
        "captcha_error" : "",
    }


        if user_captcha != real_captcha:
            context["captcha_error"] = "Captcha is incorrect."
            return render(request,"login.html",context)

        user = authenticate(
            request,
            username=username,
            password=password
        )
        
        if user is not None:
            login(request, user)

            request.session.pop("login_captcha", None)

            return redirect("notes:home")

        else:
            if not User.objects.filter(username=username).exists():
                context["username_error"] = "Username does not exist."
            else:
                context["password_error"] = "Password is incorrect.."
            return render(request,"login.html",context)
    return redirect("accounts:login_page")
    

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('notes:home'))


def signup_view(request):
    if request.method == "POST":
        user_captcha = request.POST.get("captcha")
        real_captcha = request.session.get("register_captcha")

        if user_captcha != real_captcha:
            request.session.pop("register_captcha", None)
            messages.error(request, "Captcha is incorrect.")
            return redirect("accounts:login_page")

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        phone_number = request.POST.get("phone_number")

        if User.objects.filter(username=username).exists():
            request.session.pop("register_captcha", None)
            messages.error(request, "این نام کاربری قبلاً ثبت شده")
            return redirect("accounts:login_page")

        if password1 == password2:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            Profile.objects.create(
            user=user,
            phone_number=phone_number
            )
 
            request.session.pop("register_captcha", None)
            messages.success(request, "ثبت‌نام موفق بود")
            return redirect("accounts:login_page")

        else:
            request.session.pop("register_captcha", None)
            messages.error(request, "رمزها یکسان نیستند")
            return redirect("accounts:login_page")

    return render(request,'accounts/signup.html')


def login_page(request):
    login_captcha = str(Captcha())
    register_captcha = str(Captcha())

    request.session["login_captcha"] = login_captcha
    request.session["register_captcha"] = register_captcha
    
    context = {
        "captcha1" : login_captcha,
        "captcha2" : register_captcha,
        "username_error" : "",
        "password_error" : "",
        "captcha_error" : "",
        "username": request.user.username
    }
    return render(request, "login.html", context )

    
def password_reset_view(request):
    return render(request,'profile.html')