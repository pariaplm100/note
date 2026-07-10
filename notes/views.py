from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from notes.forms import AboutusForm,ContactUsForm
from .models import Note
from notes.forms import AboutusForm, ContactUsForm
from django.contrib.auth.decorators import login_required
from .models import Note 

def ContactUs_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes:ContactUs")
    else:
        form = ContactUsForm()
        
    return render(request, "contact-us.html", {"form": form})
    
def AboutUs_view(request):
    if request.method == "POST":
        form = AboutusForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "AboutUs.html", {"form": form})
    else:
        form = AboutusForm()
    return render(request, "AboutUs.html", {"form": form})
    
@login_required    
def home(request):
    return render(request, "home.html")

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
    notes = Note.objects.filter(author=request.user)
    return render(request, 'home.html', {'notes': notes})
    
def profile_view(request):
    return render(request,'profile.html')
    
