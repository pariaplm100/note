from django.shortcuts import render, redirect 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from notes.forms import AboutusForm,ContactUsForm
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def ContactUs_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        messages.success(request, "Your message has been sent successfully. Thank you for contacting us!")
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
    if request.user.is_authenticated:
        notes = Note.objects.filter(course__author=request.user)
        courses = Course.objects.filter(author=request.user)
    else:
        notes = Note.objects.none()
        courses = []

    context = {
        "notes": notes,
        "courses": courses,
    }
    
    return render(request, "home.html", context)

@login_required
@require_POST
def create_note(request):

    name = request.POST.get("name")
    topic = request.POST.get("topic")

    course_name = request.POST.get("course_name")

    course, created = Course.objects.get_or_create(
        author=request.user,
        name=course_name
    )

    note = Note.objects.create(
        author=request.user if request.user.is_authenticated else None,
        course=course,
        name=request.POST.get("name"),
        topic=request.POST.get("topic")
    )
    
    for file in uploaded_files:
            NoteFile.objects.create(
                note=note,
                file=file
            )

    files_data = []

    for f in note.files.all():
        files_data.append({
                "name": f.file.name.split("/")[-1],
                "url": f.file.url
            })
        note_file = NoteFile.objects.create(
            note=note,
            file=file
        )

        files_data.append({
            "name": note_file.file.name.split("/")[-1],
            "url": note_file.file.url
        })


    return JsonResponse({
        "id": note.id,
        "name": note.name,
        "topic": note.topic,
        "files": files_data
    })
    return JsonResponse({"error": "Invalid request"},status=400)

@login_required
@require_POST
def delete_note(request, note_id):
    if request.method == "POST":
        note = Note.objects.get(id=note_id)
        note.name = request.POST.get("name")
        note.topic = request.POST.get("topic")
        note.save()
        files_data = []

        for f in note.files.all():
            files_data.append({
                "name": f.file.name.split("/")[-1],
                "url": f.file.url})

        return JsonResponse({"id": note.id,"name": note.name, "topic": note.topic, "files": files_data})
    return JsonResponse({"error":"invalid request"}, status=400)
    
def update_note(request, note_id):

    if request.method == "POST":
        note = Note.objects.get(id=note_id)
        note.name = request.POST.get("name")
        note.topic = request.POST.get("topic")
        note.save()
        files_data = []

        for f in note.files.all():
            files_data.append({
                "name": f.file.name.split("/")[-1],
                "url": f.file.url})

        return JsonResponse({"id": note.id,"name": note.name, "topic": note.topic, "files": files_data})
    return JsonResponse({"error":"invalid request"}, status=400)    