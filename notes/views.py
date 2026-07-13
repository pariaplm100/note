from django.shortcuts import render, redirect 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from notes.forms import AboutusForm,ContactUsForm
from .models import Note
from notes.forms import AboutusForm, ContactUsForm
from django.contrib.auth.decorators import login_required
from .models import Note 
import json

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
       
def home(request):
    return render(request, "home.html")

def profile_view(request):
    return render(request,'profile.html')
    
def home_view(request):
    notes = Note.objects.filter(author=request.user)
    context = {"notes": notes}
    return render(request, "home.html", context)

def create_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = Note.objects.create(author=request.user,name=data["name"],topic=data["topic"])
        return JsonResponse({"id": note.id,"name": note.name,"topic": note.topic})