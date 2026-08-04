from django.shortcuts import render,redirect
from accounts.captcha import Captcha
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import re
from random import randint
from time import time


def signup_context(request, username="", email="", phone_number=""):
    login_captcha = str(Captcha())
    register_captcha = str(Captcha())
    request.session["login_captcha"] = login_captcha
    request.session["register_captcha"] = register_captcha
    
    return {
        "captcha1": login_captcha,
        "captcha2": register_captcha,
        "show_login": False,
        "signup_username": username,
        "signup_email": email,
        "signup_phone": phone_number,
        "username": "",
        "username_error": "",
        "password_error": "",
        "captcha_error": "",
    }


def can_resend(request):
    last_resend = request.session.get("last_resend")
    if last_resend and time() - last_resend < 120:
        return False
    return True

def send_otp(request, email):
    otp = str(randint(100000, 999999))

    request.session["otp"] = otp
    request.session["otp_time"] = int(time())
    request.session["last_resend"] = int(time())

    send_mail(
        subject="Verification Code",
        message=f"Your verification code is: {otp}",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")
        
    if request.method == "POST":

        username = request.POST.get("username","").strip()
        password = request.POST.get("password","").strip()
        user_captcha = request.POST.get("captcha").strip()
        phone_number= request.POST.get("phone_number","").strip()

        real_captcha = request.session.get("login_captcha")
        new_login_captcha = Captcha()
        new_register_captcha = Captcha()
        request.session["login_captcha"] = new_login_captcha
        request.session["register_captcha"] = new_register_captcha
        
        context = {
        "captcha1" : new_login_captcha,
        "captcha2" : new_register_captcha,
        "username": username,
        "username_error" : "",
        "password_error" : "",
        "captcha_error" : "",
        "show_login": request.session.pop("show_login", False),
    }
        if " " in username or " " in password:
            messages.error(request, "Username and password cannot contain spaces.")
            return render(request, "login.html", context)
            
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
            messages.success(request, "Login successful.")
            request.session.pop("login_captcha", None)

            return redirect("notes:home")

        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Password is incorrect.")
                
            return render(request,"login.html",context)
            
    return redirect("accounts:login_page")
    
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        messages.error(request, "Logged out successfully.")
        logout(request)
    return redirect(reverse('notes:home'))
    
    
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")
        
    if request.method == "POST":
    
        user_captcha = request.POST.get("captcha","").strip()
        real_captcha = request.session.get("register_captcha","").strip()
        phone_number = request.POST.get("phone_number","").strip()
            
        username = request.POST.get("username","").strip()
        email = request.POST.get("email","").strip()
        password1 = request.POST.get("password1","").strip()
        password2 = request.POST.get("password2","").strip()
        phone_number = request.POST.get("phone_number","").strip()
        
            
        context = signup_context(
            request,
            username=username,
            email=email,
            phone_number=phone_number
        )
        
        if " " in username:
            messages.error(request, "Username cannot contain spaces.")
            return render(request, "login.html", context)

        if " " in password1 or " " in password2:
            messages.error(request, "Password cannot contain spaces.")
            return render(request, "login.html", context)
            
        if user_captcha != real_captcha:
            new_captcha = str(Captcha())
            request.session["register_captcha"] = new_captcha
            context["captcha2"] = new_captcha
            messages.error(request, "Captcha is incorrect.")
            return render(request, "login.html", context)
    
        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, "login.html", context)

        if len(username) < 4:
            context["signup_username"] = ""
            messages.error(request, "Username must be at least 4 characters.")
            return render(request, "login.html", context)

        if len(username) > 20:
            context["signup_username"] = ""
            messages.error(request, "Username cannot be longer than 20 characters.")
            return render(request, "login.html", context)

        validator = UnicodeUsernameValidator()
        try:
            validator(username)
        except ValidationError:
            context["signup_username"] = ""
            messages.error(request, "Invalid username.")
            return render(request, "login.html", context)

        if email:
            try:
                validate_email(email)
            except ValidationError:
                context["signup_email"] = ""
                messages.error(request, "Invalid email address.")
                return render(request, "login.html", context)

        if not re.fullmatch(r"09\d{9}", phone_number):
            context["signup_phone"] = ""
            messages.error(request, "Invalid phone number.")
            return render(request, "login.html", context)

        if User.objects.filter(username=username).exists():
            context["signup_username"] = ""
            messages.error(request, "Username already exists.")
            return render(request, "login.html", context)

        if email and User.objects.filter(email=email).exists():
            context["signup_email"] = ""
            messages.error(request, "Email is already registered.")
            return render(request, "login.html", context)

        if Profile.objects.filter(phone_number=phone_number).exists():
            context["signup_phone"] = ""
            messages.error(request, "Phone number is already registered.")
            return render(request, "login.html", context)

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

            return render(request, "login.html", context)
        
        request.session["signup_data"] = {
            "username": username,
            "email": email,
            "password": password1,
            "phone_number": phone_number,
        }
        
        send_otp(request,email) 
        
        request.session.pop("register_captcha", None)

        return redirect("accounts:verify_email")

    request.session.pop("register_captcha", None)
    return redirect("accounts:login_page")


@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect("notes:home")
        
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
        "username": request.user.username,
        "show_login": request.session.pop("show_login", False),
    }
    return render(request, "login.html", context )

    
@never_cache    
def verify_email_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")
    
    if request.method == "POST":
        
        if request.POST.get("resend"):

            data = request.session.get("signup_data")

            if data is None:
                messages.error(request, "Session expired.")
                return redirect("accounts:login_page")

            if not can_resend(request):
                messages.error(request, "Please wait 120 seconds before requesting another code.")
                
                request.session.pop("register_captcha", None)
                return redirect("accounts:verify_email")

            send_otp(request, data["email"])

            messages.success(request, "A new verification code has been sent.")
            
            request.session.pop("register_captcha", None)
            return redirect("accounts:verify_email")

        user_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        otp_time = request.session.get("otp_time")
        
        if otp_time is None:
            messages.error(request, "Verification code has expired.")
            
            request.session.pop('otp',None)
            request.session.pop('otp_time',None)
            request.session.pop('signup_data',None)
            request.session.pop("register_captcha", None)
            
            return redirect("accounts:login_page")
        
        expire_time = 120
        if time() - otp_time > expire_time:
            messages.error(request, "Verification code has expired.")
            
            request.session.pop("otp",None)
            request.session.pop("otp_time",None)
            request.session.pop("signup_data", None)
            request.session.pop("register_captcha", None)
            
            return redirect("accounts:verify_email")

        if user_otp == real_otp:

            data = request.session.get("signup_data")
            
            if data is None:
                messages.error(request,"Session expired.")
                request.session.pop("register_captcha", None)
                
                return redirect("accounts:login_page")
                
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )

            Profile.objects.create(
                user=user,
                phone_number=data["phone_number"],
            )

            request.session.pop("otp", None)
            request.session.pop("otp_time", None)
            request.session.pop("signup_data", None)
            request.session.pop("register_captcha", None)

            messages.success(request, "Account created successfully.")
            request.session["show_login"] = True

            return redirect("accounts:login_page")

        else:
            messages.error(request, "Verification code is incorrect.")
            request.session.pop("register_captcha", None)

    return render(request,"verify_email.html",{"email": request.session.get("signup_data", {}).get("email"),"last_resend": request.session.get("last_resend", 0)
    })
    
@never_cache    
def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")

    if request.method == "POST":
        username = request.POST.get("username","").strip()

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist.")
            return redirect("accounts:forgot_password")

        user = User.objects.get(username=username)

        request.session["reset_username"] = username

        send_otp(request, user.email)

        messages.success(request, "Verification code sent to your email.")
        return redirect("accounts:verify_reset_password")

    return render(request, "forgot_password.html")
    
    
@never_cache    
def verify_reset_password_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")
        
    if request.method == "POST":

        if request.POST.get("resend"):

            username = request.session.get("reset_username")

            if username is None:
                messages.error(request, "Session expired.")
                return redirect("accounts:forgot_password")

            user = User.objects.get(username=username)

            if not can_resend(request):
                messages.error(request, "Please wait 120 seconds before requesting another code.")
                return redirect("accounts:verify_reset_password")

            send_otp(request, user.email)

            messages.success(request, "A new verification code has been sent.")

            return redirect("accounts:verify_reset_password")


        user_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        otp_time = request.session.get("otp_time")

        if otp_time is None:
            messages.error(request, "Verification code has expired.")
            return redirect("accounts:forgot_password")

        if time() - otp_time > 120:

            request.session.pop("otp", None)
            request.session.pop("otp_time", None)

            messages.error(request, "Verification code has expired.")

            return redirect("accounts:verify_reset_password")

        if user_otp == real_otp:

            request.session["reset_verified"] = True

            request.session.pop("otp", None)
            request.session.pop("otp_time", None)
            messages.success(request, "Verification successful.You can change password")
            return redirect("accounts:new_password")

        messages.error(request, "Verification code is incorrect.")

    username = request.session.get("reset_username")

    email = ""

    if username:
        email = User.objects.get(username=username).email

    return render(request, "verify_reset_password.html", {
        "email": email,
        "last_resend": request.session.get("last_resend", 0),
        "last_resend": request.session.get("last_resend", 0),
    })

@never_cache 
def new_password_view(request):
    if request.user.is_authenticated:
        return redirect("notes:home")

    if not request.session.get("reset_verified"):
        return redirect("accounts:forgot_password")

    if request.method == "POST":
        password1 = request.POST.get("password1","").strip()
        password2 = request.POST.get("password2","").strip()

        if " " in password1 or " " in password2:
            messages.error(request, "Password cannot contain spaces.")
            return redirect("accounts:new_password")
            
        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return redirect("accounts:new_password")

        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return redirect("accounts:new_password")

        username = request.session.get("reset_username")

        user = User.objects.get(username=username)

        user.set_password(password1)
        user.save()

        request.session.pop("reset_username", None)
        request.session.pop("reset_verified", None)

        messages.success(request, "Password changed successfully.")

        request.session["show_login"] = True
        return redirect("accounts:login_page")

    return render(request, "reset_password.html")