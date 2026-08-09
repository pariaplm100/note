from django.urls import path,include
from django.contrib import admin
from notes.feed import LatestEntriesFeed,LatestEntriesFeed2,LatestEntriesFeed3
from notes import views

app_name = "notes"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("AboutUs/", views.AboutUs_view, name="AboutUs"),
    path("ContactUs/", views.ContactUs_view, name="ContactUs"),
    path('profile/',views.profile_view,name='profile'),
    path("create-note/", views.create_note, name="create_note"),
    path("delete-note/<int:note_id>/",views.delete_note,name="delete_note"),
    path("update-note/<int:note_id>/", views.update_note, name="update_note"),
    path("verify_delete_account",views.verify_delete_account_view,name="verify_delete_account"),
    path("delete-account/",views.delete_account,name="delete_account"),
    path("confirm_delete_account",views.confirm_delete_account,name= 'confirm_delete_account'),
    path("view-profile/",views.view_profile,name="view_profile"),
    path("edit-profile/",views.edit_profile,name="edit_profile"),
    path("Course&Notes/", views.courses_notes, name="Course_Notes"),
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
    path("create-note-page", views.create_note_in_CourseNote, name="create_note_in_CourseNote"),
    path("edite-course_notes/<int:note_id>/", views.edit_course_notes, name="edit_course_notes"),
    path("delete-file/<int:file_id>/", views.delete_file, name="delete_file"),
    path("note-files/<int:id>/", views.note_files, name="note_files"),
    path("home-notes-api/", views.home_notes_api, name="home_notes_api"),
    path('rss/feed/', LatestEntriesFeed()),
    path('rss/courses/', LatestEntriesFeed2()),
    path('rss/files/', LatestEntriesFeed3()),
    path("news/note/<int:pk>/", views.news_item, name="news-item"),
    path("news/course/<int:pk>/", views.news_item2, name="news-item2"),
    path("news/file/<int:pk>/", views.news_item3, name="news-item3"),
]