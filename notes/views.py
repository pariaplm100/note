from django.shortcuts import render, redirect 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from notes.forms import AboutusForm,ContactUsForm
from .models import *
from django.views.decorators.http import require_POST

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
    if not request.session.session_key:
        request.session.create()
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user)
    else:
        notes = Note.objects.filter(session_key=request.session.session_key)

    context = {"notes": notes}
    return render(request, "home.html", context)

def create_note(request):
    if request.method == "POST":
        
        if not request.session.session_key:
            request.session.create()

        

        name = request.POST.get("name")
        topic = request.POST.get("topic")
        uploaded_files = request.FILES.getlist("files")

        note = Note.objects.create( 
            author=request.user if request.user.is_authenticated else None,
            session_key = request.session.session_key,
            name=name,
           topic=topic)
        for file in uploaded_files:
            NoteFile.objects.create(
                note=note,
                file=file
            )

        files_data = []

        for f in note.files.all():
            files_data.append({
                "name": f.file.name.split("/")[-1], #برگرداندن اخرین مقدار که شامل همان فایل است.
                "url": f.file.url  #ادرس برای رای دانلود یا باز کردن فایل
            })

        return JsonResponse({
            "id": note.id,
            "name": note.name,
            "topic": note.topic,
            "files": files_data
            })

    return JsonResponse({"error": "Invalid request"},status=400)

@require_POST
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return JsonResponse({"success": True})