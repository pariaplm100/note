from django.shortcuts import render,redirect
from accounts.captcha import Captcha
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Profile
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
import re

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
        
            
        #if not re.fullmatch(r"09\d{9}", phone_number):
            #messages.error(request,"Invalid phone number.")
            #request.session.pop("login_captcha", None)
            #return redirect("accounts:login_page")    
        

        if user_captcha != real_captcha:
            messages.error(request, "Captcha is incorrect.")
            return render(request,"login.html",context)
            
        #if email:
            #try:
                #validate_email(email)
            #except ValidationError:
                #messages.error(request, "Invalid email address.")
                #request.session.pop("login_captcha", None)
                #return redirect("accounts:login_page")    

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
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Password is incorrect.")
                
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
        
        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")
            
        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")

        if len(username) > 20:
            messages.error(request, "Username cannot be longer than 20 characters.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")    
            
        validator = UnicodeUsernameValidator()
        try:
            validator(username)
        except ValidationError:
            messages.error(request, "Invalid username.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")   
            
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Invalid email address.")
                request.session.pop("register_captcha", None)
                return redirect("accounts:login_page")    
                
        if not re.fullmatch(r"09\d{9}", phone_number):
            messages.error(request,"Invalid phone number.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")      
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")   
            
        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page") 
            
        if Profile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number is already registered.")
            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")    

        try:
            validate_password(password1)
        except ValidationError as e:
            errors = " ".join(e.messages)
            if "too short" in errors:
                messages.error(request, "Password is too short.")
            elif "too common" in errors:
                messages.error(request, "Password is too common.")
            elif "entirely numeric" in errors:
                messages.error(request, "Password cannot be only numbers.")
            else:
                messages.error(request, "Invalid password.")

            request.session.pop("register_captcha", None)
            return redirect("accounts:login_page")
            
        
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
        messages.success(request, "Sign up successful.")
        return redirect("accounts:login_page")

    request.session.pop("register_captcha", None)
    return redirect('accounts:login_page')


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