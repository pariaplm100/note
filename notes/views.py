from django.shortcuts import render, redirect 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from notes.forms import AboutusForm,ContactUsForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from .models import Course, Note
from random import randint
from time import time
from .models import *
from accounts.models import Profile

@login_required
def courses_notes(request):
    search = request.GET.get("search", "").strip()
    notes = Note.objects.filter(author=request.user).annotate(
        files_count = Count("files") ).order_by("-create_time") 

    if search:
        notes = notes.filter(
            Q(name__icontains=search) |
            Q(topic__icontains=search) )

    paginator = Paginator(notes, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj,"search": search}

    return render(request, "courses_notes.html", context)

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
    

def ContactUs_view(request):

    if request.user.is_authenticated:
        courses = Course.objects.filter(author=request.user)
    else:
        courses = Course.objects.none()

    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been sent successfully. Thank you for contacting us!"
            )
            return redirect("notes:ContactUs")
    else:
        form = ContactUsForm()

    return render(request, "contact-us.html", {
        "form": form,
        "courses": courses,
    })
    
    
    
def AboutUs_view(request):
    if request.user.is_authenticated:
        courses = Course.objects.filter(author=request.user)
    else:
        courses = Course.objects.none()

    if request.method == "POST":
        form = AboutusForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = AboutusForm()

    return render(request, "AboutUs.html", { "form": form, "courses": courses,})
     
       
       
def home(request):
    return render(request, "home.html")


@login_required
def profile_view(request):
    
    profile = Profile.objects.get(user = request.user)
     
    return render(request,'profile.html',{"profile":profile})
    
    
def home_view(request):
    search = request.GET.get("search","").strip()
    if request.user.is_authenticated:
        notes = Note.objects.filter(course__author=request.user)
        
        if search:
            notes = notes.filter(
                Q(name__icontains = search) |
                Q(topic__icontains = search)
            )
            
        courses = Course.objects.filter(author=request.user)
    else:
        notes = Note.objects.none()
        courses = Course.objects.none()

    context = {
        "notes": notes,
        "courses": courses,
        "search": search,
    }
    
    return render(request, "home.html", context)

@login_required
def home_notes_api(request):

    notes = Note.objects.filter(course__author=request.user).order_by("-create_time")

    data = []

    for note in notes:
        data.append({
            "id": note.id,
            "name": note.name,
            "topic": note.topic,
        })

    return JsonResponse({"notes": data})

@login_required
@require_POST
def create_note(request):
    
    uploaded_files = request.FILES.getlist("files")
    
    name = request.POST.get("name")
    topic = request.POST.get("topic")

    course_name = request.POST.get("course_name")

    course, created = Course.objects.get_or_create(
        author=request.user,
        name=course_name
    )

    note = Note.objects.create(
        author=request.user,
        course=course,
        name=name,
        topic=topic,
    )
    
    for file in uploaded_files:
        NoteFile.objects.create(
            note=note,
            file=file
        )
    
    files_data = []
    
    
    for f in note.files.all().order_by("-create_time"):
        files_data.append({
            "id": f.id,
            "name": f.file.name.split("/")[-1],
            "url": f.file.url
        })

    return JsonResponse({
        "id": note.id,
        "name": note.name,
        "topic": note.topic,
        "files": files_data,
        "course_id": course.id,
        "course_name": course.name,
    })
    

@login_required
@require_POST
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id  ,  author=request.user)
        
        course = note.course
        course_id = note.course.id
        note.delete()
        course_deleted = False
        
        if not course.notes.exists():
            course.delete()
            course_deleted = True

        return JsonResponse({"success": True,
                             "course_id": course_id,
                             "course_deleted": course_deleted})
    except Note.DoesNotExist:
        return JsonResponse({"success": False,"error": "Note not found"}, status=404)

    
@login_required
@require_POST
def delete_file(request, file_id):

    file = get_object_or_404(
        NoteFile,
        id=file_id,
        note__author=request.user
    )

    file.delete()

    return JsonResponse({
        "success": True,
        "file_id": file_id,
    })

@login_required
def create_note_in_CourseNote(request):

    if request.method == "POST":

        course_name = request.POST.get("course_name")
        topic = request.POST.get("topic")
        uploaded_files = request.FILES.getlist("files")

        course, created = Course.objects.get_or_create(
            author=request.user,
            name=course_name
        )

        note = Note.objects.create(
            author=request.user,
            course=course,
            name=course_name,
            topic=topic,
        )

        for file in uploaded_files:
            NoteFile.objects.create(
                note=note,
                file=file
            )

        messages.success(request, "Note created successfully.")
        return redirect("notes:Course_Notes")

    return render(request, "create_note_in_CourseNote.html")



@login_required
def edit_course_notes(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        author=request.user
    )

    if request.method == "POST":

        course_name = request.POST.get("course_name","").strip()
        
        if course_name:
            note.course.name = course_name
            note.course.save()
                    
        note.name = request.POST.get("course_name")
        note.topic = request.POST.get("topic")
        note.save()

        uploaded_files = request.FILES.getlist("files")

        for file in uploaded_files:
            NoteFile.objects.create(
                note=note,
                file=file
            )

        return redirect("notes:note_detail", note_id=note.id)

    context = {
        "note": note,
    }

    return render(request, "edit_course_notes.html", context)
    
    
@login_required
@require_POST    
def update_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, author=request.user)

        course_name = request.POST.get("course_name")
        if course_name:
            note.course.name = course_name
            note.course.save()
            
        note.name = request.POST.get("course_name")
        note.topic = request.POST.get("topic")
        note.save()
        uploaded_files = request.FILES.getlist("files")
        
        for f in uploaded_files:
            NoteFile.objects.create(note=note, file=f)
        
        files_data = []

        for f in note.files.all().order_by("-create_time"):
            files_data.append({
                "id":f.id,
                "name": f.file.name.split("/")[-1],
                "url": f.file.url
            })

        return JsonResponse({
            "id": note.id,
            "name": note.name,
            "topic": note.topic,
            "course_id":note.course.id,
            "course_name":note.course.name,
            "files": files_data,
        })

    except Note.DoesNotExist:
        return JsonResponse({
            "error": "Note not found"
        }, status=404)
        

def note_files(request, id):
    note = Note.objects.get(id=id)
    files = []
    
    for f in note.files.all().order_by("-create_time"):
        files.append({
            "id": f.id,
            "name": f.file.name.split("/")[-1],
            "url": f.file.url
        })

    return JsonResponse({"files": files})

       
@login_required
def confirm_delete_account(request):
    return render(request, "confirm_delete_account.html")    
    
    
@login_required
def delete_account(request):
    send_otp(request, request.user.email)
    return redirect("notes:verify_delete_account")    
    

@login_required
@never_cache
def verify_delete_account_view(request):

    if request.method == "POST":

        if request.POST.get("resend"):
            if not can_resend(request):
                messages.error(request,"Please wait 60 seconds before requesting another code.")
                return redirect("notes:verify_delete_account")

            send_otp(request, request.user.email)

            messages.success(
                request,
                "A new verification code has been sent."
            )

            return redirect("notes:verify_delete_account")

        user_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        otp_time = request.session.get("otp_time")

        if otp_time is None:
            messages.error(request, "Verification code has expired.")
            return redirect("notes:profile")

        if time() - otp_time > 120:

            request.session.pop("otp", None)
            request.session.pop("otp_time", None)

            messages.error(request, "Verification code has expired.")

            return redirect("notes:verify_delete_account")

        if user_otp == real_otp:

            request.session.pop("otp", None)
            request.session.pop("otp_time", None)

            user = request.user

            logout(request)
            user.delete()

            messages.success(
                request,
                "Your account has been deleted successfully."
            )

            return redirect("notes:home")

        messages.error(request, "Verification code is incorrect.")

    return render(request, "verify_delete_account.html", {
        "email": request.user.email,
        "last_resend": request.session.get("last_resend", 0),
    })
    

@login_required
def view_profile(request):

    profile = request.user.profile

    courses_count = Course.objects.filter(author=request.user).count()

    notes_count = Note.objects.filter(author=request.user).count()

    context = {
        "profile": profile,
        "courses_count": courses_count,
        "notes_count": notes_count,
    }

    return render(request,"view_profile.html",context)
    
@login_required
def note_detail(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        author=request.user
    )

    return render(
        request,
        "note_detail.html",
        {
            "note": note
        }
    )
    
    
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        username = request.POST.get("username").strip()
        bio = request.POST.get("bio","")
        
        if " " in username:
            messages.error(request, "Username cannot contain spaces.")
            return render(request, "edit_profile.html", {"profile": profile})
            
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "This username is already taken.")
            return render(request, "edit_profile.html", {"profile": profile})
        
        request.user.username = username
        request.user.save()
        
        profile.bio = bio

        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("notes:view_profile")

    return render(request, "edit_profile.html", {"profile": profile})


def news_item(request, pk):
    pass

def news_item2(request, pk):
    pass

def news_item3(request, pk):
    pass