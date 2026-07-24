from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Course, Note, NoteFile, ContactUs, AboutUs
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from unittest.mock import patch
from time import time


class CourseModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

    def test_course_created(self):
        self.assertEqual(Course.objects.count(), 1)

    def test_course_name_saved(self):
        self.assertEqual(self.course.name, "Python")

    def test_course_author(self):
        self.assertEqual(self.course.author, self.user)

    def test_course_create_time_exists(self):
        self.assertIsNotNone(self.course.create_time)

    def test_course_update_time_exists(self):
        self.assertIsNotNone(self.course.update_time)

    def test_delete_user_deletes_course(self):
        self.user.delete()
        self.assertEqual(Course.objects.count(), 0)


class NoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Lesson 1",
            topic="Introduction"
        )

    def test_note_created(self):
        self.assertEqual(Note.objects.count(), 1)

    def test_note_author(self):
        self.assertEqual(self.note.author, self.user)

    def test_note_course(self):
        self.assertEqual(self.note.course, self.course)

    def test_note_default_status(self):
        self.assertTrue(self.note.status)

    def test_note_create_time_exists(self):
        self.assertIsNotNone(self.note.create_time)

    def test_note_update_time_exists(self):
        self.assertIsNotNone(self.note.update_time)

    def test_note_str(self):
        self.assertIn("Lesson 1", str(self.note))

    def test_delete_course_deletes_note(self):
        self.course.delete()
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_user_deletes_note(self):
        self.user.delete()
        self.assertEqual(Note.objects.count(), 0)


class NoteFileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Lesson",
            topic="Topic"
        )

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world"
        )

        self.note_file = NoteFile.objects.create(
            note=self.note,
            file=file
        )

    def test_note_file_created(self):
        self.assertEqual(NoteFile.objects.count(), 1)

    def test_note_file_relation(self):
        self.assertEqual(self.note_file.note, self.note)

    def test_delete_note_deletes_file(self):
        self.note.delete()
        self.assertEqual(NoteFile.objects.count(), 0)


class ContactUsModelTest(TestCase):

    def test_contact_created(self):

        contact = ContactUs.objects.create(
            full_name="Arya",
            email="arya@test.com",
            phone_number="09123456789",
            message="Hello"
        )

        self.assertEqual(
            str(contact),
            "Arya"
        )


class AboutUsModelTest(TestCase):

    def test_about_created(self):

        about = AboutUs.objects.create(
            name="Arya",
            email="arya@test.com",
            message="Hello"
        )

        self.assertEqual(
            str(about),
            "Arya"
        )



from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Course, Note


class CreateNoteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

    def login(self):
        self.client.login(
            username="arya",
            password="Test12345"
        )

    def test_login_required(self):

        response = self.client.post(
            reverse("notes:create_note")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


    def test_create_note_success(self):

        self.login()

        response = self.client.post(
            reverse("notes:create_note"),
            {
                "course_name": "Python",
                "name": "Lesson 1",
                "topic": "Variables",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Course.objects.count(),
            1
        )

        self.assertEqual(
            Note.objects.count(),
            1
        )

        note = Note.objects.first()

        self.assertEqual(
            note.name,
            "Lesson 1"
        )

        self.assertEqual(
            note.topic,
            "Variables"
        )


    def test_existing_course_not_created_again(self):

        self.login()

        Course.objects.create(
            name="Python",
            author=self.user
        )

        self.client.post(
            reverse("notes:create_note"),
            {
                "course_name": "Python",
                "name": "Lesson 2",
                "topic": "Functions",
            }
        )

        self.assertEqual(
            Course.objects.count(),
            1
        )


    def test_json_response(self):

        self.login()

        response = self.client.post(
            reverse("notes:create_note"),
            {
                "course_name": "Python",
                "name": "Lesson 1",
                "topic": "Variables",
            }
        )

        data = response.json()

        self.assertEqual(
            data["name"],
            "Lesson 1"
        )

        self.assertEqual(
            data["topic"],
            "Variables"
        )

        self.assertEqual(
            data["course_name"],
            "Python"
        )
        
    def test_create_note_with_file(self):

        self.login()

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        response = self.client.post(
            reverse("notes:create_note"),
            {
                "course_name": "Python",
                "name": "Lesson File",
                "topic": "Files",
                "files": file,
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            NoteFile.objects.count(),
            1
        )


        note = Note.objects.first()

        self.assertEqual(
            note.files.count(),
            1
        )



def test_create_note_with_multiple_files(self):

    self.login()

    file1 = SimpleUploadedFile(
        "one.txt",
        b"file one",
        content_type="text/plain"
    )

    file2 = SimpleUploadedFile(
        "two.txt",
        b"file two",
        content_type="text/plain"
    )


    response = self.client.post(
        reverse("notes:create_note"),
        {
            "course_name": "Python",
            "name": "Multiple Files",
            "topic": "Upload",
            "files": [file1, file2],
        }
    )


    self.assertEqual(
        response.status_code,
        200
    )


    self.assertEqual(
        NoteFile.objects.count(),
        2
    )


    note = Note.objects.first()

    self.assertEqual(
        note.files.count(),
        2
    )



def test_response_contains_files(self):

    self.login()


    file = SimpleUploadedFile(
        "test.txt",
        b"hello",
        content_type="text/plain"
    )


    response = self.client.post(
        reverse("notes:create_note"),
        {
            "course_name": "Python",
            "name": "Lesson",
            "topic": "Topic",
            "files": file,
        }
    )


    data = response.json()


    self.assertEqual(
        len(data["files"]),
        1
    )


    self.assertEqual(
        data["files"][0]["name"],
        "test.txt"
    )
    


class DeleteNoteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Lesson 1",
            topic="Variables"
        )


    def login(self):
        self.client.login(
            username="arya",
            password="Test12345"
        )


    def test_login_required(self):

        response = self.client.post(
            reverse(
                "notes:delete_note",
                args=[self.note.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )



    def test_delete_note_success(self):

        self.login()

        response = self.client.post(
            reverse(
                "notes:delete_note",
                args=[self.note.id]
            )
        )

        data = response.json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            Note.objects.count(),
            0
        )



    def test_delete_course_when_last_note_deleted(self):

        self.login()

        self.client.post(
            reverse(
                "notes:delete_note",
                args=[self.note.id]
            )
        )


        self.assertEqual(
            Course.objects.count(),
            0
        )



    def test_course_not_deleted_if_has_other_notes(self):

        Note.objects.create(
            author=self.user,
            course=self.course,
            name="Lesson 2",
            topic="Functions"
        )

        self.login()

        self.client.post(
            reverse(
                "notes:delete_note",
                args=[self.note.id]
            )
        )


        self.assertEqual(
            Course.objects.count(),
            1
        )



    def test_cannot_delete_other_user_note(self):

        other_course = Course.objects.create(
            name="Django",
            author=self.other_user
        )

        other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Private",
            topic="Test"
        )


        self.login()

        response = self.client.post(
            reverse(
                "notes:delete_note",
                args=[other_note.id]
            )
        )


        self.assertEqual(
            response.status_code,
            404
        )
        
        


class UpdateNoteViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Old Name",
            topic="Old Topic"
        )


    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )


    def test_login_required(self):

        response = self.client.post(
            reverse(
                "notes:update_note",
                args=[self.note.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )



    def test_update_note_success(self):

        self.login()

        response = self.client.post(
            reverse(
                "notes:update_note",
                args=[self.note.id]
            ),
            {
                "course_name": "Django",
                "topic": "Updated Topic"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.note.refresh_from_db()


        self.assertEqual(
            self.note.topic,
            "Updated Topic"
        )


        self.assertEqual(
            self.note.course.name,
            "Django"
        )



    def test_update_add_file(self):

        self.login()


        file = SimpleUploadedFile(
            "new.txt",
            b"hello",
            content_type="text/plain"
        )


        response = self.client.post(
            reverse(
                "notes:update_note",
                args=[self.note.id]
            ),
            {
                "course_name": "Python",
                "topic": "Files",
                "files": file
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            self.note.files.count(),
            1
        )



    def test_update_invalid_note(self):

        self.login()

        response = self.client.post(
            reverse(
                "notes:update_note",
                args=[9999]
            ),
            {
                "course_name":"Test",
                "topic":"Test"
            }
        )


        self.assertEqual(
            response.status_code,
            404
        )



    def test_cannot_update_other_user_note(self):

        other_course = Course.objects.create(
            name="Java",
            author=self.other_user
        )


        other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Private",
            topic="Secret"
        )


        self.login()


        response = self.client.post(
            reverse(
                "notes:update_note",
                args=[other_note.id]
            ),
            {
                "course_name":"Hack",
                "topic":"Changed"
            }
        )


        self.assertEqual(
            response.status_code,
            404
        )
        
        
        

class DeleteFileViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )


        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )


        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Lesson",
            topic="Test"
        )


        self.file = NoteFile.objects.create(
            note=self.note,
            file="notes_files/test.txt"
        )


    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )


    def test_login_required(self):

        response = self.client.post(
            reverse(
                "notes:delete_file",
                args=[self.file.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )



    def test_delete_file_success(self):

        self.login()


        response = self.client.post(
            reverse(
                "notes:delete_file",
                args=[self.file.id]
            )
        )


        data = response.json()


        self.assertTrue(
            data["success"]
        )


        self.assertEqual(
            NoteFile.objects.count(),
            0
        )



    def test_delete_other_user_file(self):

        other_course = Course.objects.create(
            name="Java",
            author=self.other_user
        )


        other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Other",
            topic="Secret"
        )


        other_file = NoteFile.objects.create(
            note=other_note,
            file="notes_files/other.txt"
        )


        self.login()


        response = self.client.post(
            reverse(
                "notes:delete_file",
                args=[other_file.id]
            )
        )


        self.assertEqual(
            response.status_code,
            404
        )



    def test_delete_file_not_found(self):

        self.login()


        response = self.client.post(
            reverse(
                "notes:delete_file",
                args=[9999]
            )
        )


        self.assertEqual(
            response.status_code,
            404
        )   
        
        
        
class HomeViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )


        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )


        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Django Basics",
            topic="Models and Views"
        )


        other_course = Course.objects.create(
            name="Java",
            author=self.other_user
        )


        self.other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Java Note",
            topic="OOP"
        )



    def test_guest_user(self):

        response = self.client.get(
            reverse("notes:home")
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            len(response.context["notes"]),
            0
        )


        self.assertEqual(
            len(response.context["courses"]),
            0
        )



    def test_logged_user_sees_own_notes(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )


        response = self.client.get(
            reverse("notes:home")
        )


        notes = response.context["notes"]


        self.assertIn(
            self.note,
            notes
        )


        self.assertNotIn(
            self.other_note,
            notes
        )



    def test_search_by_name(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )


        response = self.client.get(
            reverse("notes:home"),
            {
                "search":"Django"
            }
        )


        self.assertIn(
            self.note,
            response.context["notes"]
        )



    def test_search_by_topic(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )


        response = self.client.get(
            reverse("notes:home"),
            {
                "search":"Models"
            }
        )


        self.assertIn(
            self.note,
            response.context["notes"]
        )             
        
        
        
        
        
class CoursesNotesViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )


        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )


        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Django",
            topic="Models"
        )


        other_course = Course.objects.create(
            name="Java",
            author=self.other_user
        )


        self.other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Java",
            topic="OOP"
        )



    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )



    def test_login_required(self):

        response = self.client.get(
            reverse("notes:Course_Notes")
        )


        self.assertEqual(
            response.status_code,
            302
        )



    def test_user_notes_displayed(self):

        self.login()


        response = self.client.get(
            reverse("notes:Course_Notes")
        )


        self.assertIn(
            self.note,
            response.context["page_obj"]
        )



    def test_other_user_notes_not_displayed(self):

        self.login()


        response = self.client.get(
            reverse("notes:Course_Notes")
        )


        self.assertNotIn(
            self.other_note,
            response.context["page_obj"]
        )



    def test_search_name(self):

        self.login()


        response = self.client.get(
            reverse("notes:Course_Notes"),
            {
                "search":"Django"
            }
        )


        self.assertIn(
            self.note,
            response.context["page_obj"]
        )



    def test_search_topic(self):

        self.login()


        response = self.client.get(
            reverse("notes:Course_Notes"),
            {
                "search":"Models"
            }
        )


        self.assertIn(
            self.note,
            response.context["page_obj"]
        )



    def test_pagination(self):

        self.login()


        for i in range(10):

            Note.objects.create(
                author=self.user,
                course=self.course,
                name=f"Note {i}",
                topic="Test"
            )


        response = self.client.get(
            reverse("notes:Course_Notes")
        )


        self.assertTrue(
            response.context["page_obj"].paginator.num_pages > 1
        )        
        
        
        
class NoteDetailViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )


        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )


        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Django",
            topic="Models"
        )


        other_course = Course.objects.create(
            name="Java",
            author=self.other_user
        )


        self.other_note = Note.objects.create(
            author=self.other_user,
            course=other_course,
            name="Java",
            topic="OOP"
        )



    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )



    def test_login_required(self):

        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[self.note.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )



    def test_note_detail_success(self):

        self.login()


        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[self.note.id]
            )
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            response.context["note"],
            self.note
        )



    def test_other_user_note_not_accessible(self):

        self.login()


        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[self.other_note.id]
            )
        )


        self.assertEqual(
            response.status_code,
            404
        )



    def test_note_not_found(self):

        self.login()


        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[9999]
            )
        )


        self.assertEqual(
            response.status_code,
            404
        )        
        
        
        

class ViewProfileTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="09123456789"
        )


        self.course1 = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.course2 = Course.objects.create(
            name="Django",
            author=self.user
        )


        Note.objects.create(
            author=self.user,
            course=self.course1,
            name="Note 1",
            topic="Test"
        )

        Note.objects.create(
            author=self.user,
            course=self.course2,
            name="Note 2",
            topic="Test"
        )



    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )



    def test_login_required(self):

        response = self.client.get(
            reverse("notes:view_profile")
        )


        self.assertEqual(
            response.status_code,
            302
        )



    def test_profile_display(self):

        self.login()


        response = self.client.get(
            reverse("notes:view_profile")
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            response.context["profile"],
            self.profile
        )



    def test_courses_count(self):

        self.login()


        response = self.client.get(
            reverse("notes:view_profile")
        )


        self.assertEqual(
            response.context["courses_count"],
            2
        )



    def test_notes_count(self):

        self.login()


        response = self.client.get(
            reverse("notes:view_profile")
        )


        self.assertEqual(
            response.context["notes_count"],
            2
        )     
        
        
        
        
class EditProfileViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="09123456789"
        )


        self.other_user = User.objects.create_user(
            username="ali",
            password="Test12345"
        )



    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )



    def test_login_required(self):

        response = self.client.get(
            reverse("notes:edit_profile")
        )


        self.assertEqual(
            response.status_code,
            302
        )



    def test_get_edit_profile(self):

        self.login()


        response = self.client.get(
            reverse("notes:edit_profile")
        )


        self.assertEqual(
            response.status_code,
            200
        )



    def test_update_profile_success(self):

        self.login()


        response = self.client.post(
            reverse("notes:edit_profile"),
            {
                "username": "newarya",
                "bio": "My Bio"
            }
        )


        self.assertRedirects(
            response,
            reverse("notes:view_profile")
        )


        self.user.refresh_from_db()
        self.profile.refresh_from_db()


        self.assertEqual(
            self.user.username,
            "newarya"
        )


        self.assertEqual(
            self.profile.bio,
            "My Bio"
        )



    def test_username_contains_space(self):

        self.login()


        response = self.client.post(
            reverse("notes:edit_profile"),
            {
                "username": "ary a",
                "bio": "test"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.user.refresh_from_db()


        self.assertEqual(
            self.user.username,
            "arya"
        )



    def test_duplicate_username(self):

        self.login()


        response = self.client.post(
            reverse("notes:edit_profile"),
            {
                "username": "ali",
                "bio": "test"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.user.refresh_from_db()


        self.assertEqual(
            self.user.username,
            "arya"
        )



    def test_upload_profile_image(self):

        self.login()


        image = SimpleUploadedFile(
            "profile.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )


        response = self.client.post(
            reverse("notes:edit_profile"),
            {
                "username": "arya",
                "bio": "test",
                "image": image
            }
        )


        self.assertRedirects(
            response,
            reverse("notes:view_profile")
        )


        self.profile.refresh_from_db()


        self.assertTrue(
            self.profile.image.name.startswith(
                "profile_images/"
            )
        )

        self.assertTrue(
            self.profile.image.name.endswith(
                ".jpg"
            )
        )
        
        
  
  
class ContactUsViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )


    def test_contact_get(self):

        response = self.client.get(
            reverse("notes:ContactUs")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_contact_success(self):

        response = self.client.post(
            reverse("notes:ContactUs"),
            {
                "full_name":"Arya",
                "email":"arya@test.com",
                "phone_number":"09123456789",
                "message":"Hello"
            }
        )


        self.assertEqual(
            response.status_code,
            302
        )


        self.assertEqual(
            ContactUs.objects.count(),
            1
        )


    def test_contact_invalid(self):

        response = self.client.post(
            reverse("notes:ContactUs"),
            {
                "full_name":"",
                "email":"bad",
                "message":""
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )
        
        
        
class AboutUsViewTest(TestCase):


    def test_about_get(self):

        response = self.client.get(
            reverse("notes:AboutUs")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_about_success(self):

        response = self.client.post(
            reverse("notes:AboutUs"),
            {
                "name":"Arya",
                "email":"arya@test.com",
                "message":"About message"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertEqual(
            AboutUs.objects.count(),
            1
        )
        
        
        
class VerifyDeleteAccountTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            email="arya@test.com",
            password="Test12345"
        )

        self.client.login(
            username="arya",
            password="Test12345"
        )


        session = self.client.session
        session["otp"] = "123456"
        session["otp_time"] = int(time())
        session.save()



    def test_wrong_otp(self):

        response = self.client.post(
            reverse("notes:verify_delete_account"),
            {
                "otp":"999999"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertTrue(
            User.objects.filter(
                username="arya"
            ).exists()
        )



    def test_expired_otp(self):

        session = self.client.session
        session["otp_time"] = int(time()) - 200
        session.save()


        response = self.client.post(
            reverse("notes:verify_delete_account"),
            {
                "otp":"123456"
            }
        )


        self.assertRedirects(
            response,
            reverse("notes:verify_delete_account")
        )



    def test_delete_account_success(self):

        response = self.client.post(
            reverse("notes:verify_delete_account"),
            {
                "otp":"123456"
            }
        )


        self.assertRedirects(
            response,
            reverse("notes:home")
        )


        self.assertFalse(
            User.objects.filter(
                username="arya"
            ).exists()
        )



    @patch("notes.views.send_otp")
    def test_resend_success(self, mock_send):

        session = self.client.session
        session["last_resend"] = int(time()) - 200
        session.save()


        response = self.client.post(
            reverse("notes:verify_delete_account"),
            {
                "resend":"1"
            }
        )


        mock_send.assert_called_once()


        self.assertRedirects(
            response,
            reverse("notes:verify_delete_account")
        )      
        
        
        
class EditCourseNotesViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.course = Course.objects.create(
            name="Python",
            author=self.user
        )

        self.note = Note.objects.create(
            author=self.user,
            course=self.course,
            name="Python",
            topic="Old Topic"
        )

    def login(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )

    def test_login_required(self):

        response = self.client.get(
            reverse(
                "notes:edit_course_notes",
                args=[self.note.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_get_page(self):

        self.login()

        response = self.client.get(
            reverse(
                "notes:edit_course_notes",
                args=[self.note.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_edit_success(self):

        self.login()

        response = self.client.post(
            reverse(
                "notes:edit_course_notes",
                args=[self.note.id]
            ),
            {
                "course_name": "AI",
                "topic": "Machine Learning"
            }
        )

        self.assertRedirects(
            response,
            reverse(
                "notes:note_detail",
                args=[self.note.id]
            )
        )

        self.note.refresh_from_db()
        self.course.refresh_from_db()

        self.assertEqual(
            self.note.name,
            "AI"
        )

        self.assertEqual(
            self.note.topic,
            "Machine Learning"
        )

        self.assertEqual(
            self.course.name,
            "AI"
        )

    def test_note_not_found(self):

        self.login()

        response = self.client.get(
            reverse(
                "notes:edit_course_notes",
                args=[999]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )
        
        
        
        
class CreateNoteInCourseNoteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

    def login(self):
        self.client.login(
            username="arya",
            password="Test12345"
        )

    def test_login_required(self):

        response = self.client.get(
            reverse("notes:create_note_in_CourseNote")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_get_page(self):

        self.login()

        response = self.client.get(
            reverse("notes:create_note_in_CourseNote")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_create_note_success(self):

        self.login()

        response = self.client.post(
            reverse("notes:create_note_in_CourseNote"),
            {
                "course_name": "Python",
                "topic": "Django"
            }
        )

        self.assertRedirects(
            response,
            reverse("notes:Course_Notes")
        )

        self.assertEqual(
            Course.objects.count(),
            1
        )

        self.assertEqual(
            Note.objects.count(),
            1
        )

        note = Note.objects.first()

        self.assertEqual(
            note.name,
            "Python"
        )

        self.assertEqual(
            note.topic,
            "Django"
        )                