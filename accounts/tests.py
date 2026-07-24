from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from accounts.models import Profile
from django.contrib.auth import authenticate
from django.urls import reverse
from unittest.mock import patch
from time import time


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="09123456789"
        )

    def test_profile_created(self):
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_user_relation(self):
        self.assertEqual(self.profile.user, self.user)

    def test_phone_number_saved(self):
        self.assertEqual(
            self.profile.phone_number,
            "09123456789"
        )

    def test_default_image(self):
        self.assertEqual(
            self.profile.image.name,
            "default_profile/default_profile.png.webp"
        )

    def test_default_bio(self):
        self.assertEqual(self.profile.bio, "")

    def test_str_method(self):
        self.assertEqual(
            str(self.profile),
            self.user.username
        )

    def test_delete_user_deletes_profile(self):
        self.user.delete()
        self.assertEqual(Profile.objects.count(), 0)

    def test_phone_number_is_unique(self):
        user2 = User.objects.create_user(
            username="ali",
            password="Test12345"
        )

        with self.assertRaises(IntegrityError):
            Profile.objects.create(
                user=user2,
                phone_number="09123456789"
            )

    def test_blank_phone_number_allowed(self):
        user2 = User.objects.create_user(
            username="reza",
            password="Test12345"
        )

        profile = Profile.objects.create(
            user=user2
        )

        self.assertEqual(profile.phone_number, "")

    def test_blank_bio_allowed(self):
        self.assertTrue(self.profile.bio == "")


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

    def test_get_request_redirects(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertRedirects(
            response,
            reverse("accounts:login_page")
        )

    def test_authenticated_user_redirect(self):
        self.client.login(
            username="arya",
            password="Test12345"
        )

        response = self.client.post(reverse("accounts:login"))

        self.assertRedirects(
            response,
            reverse("notes:home")
        )

    def test_login_success(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "arya",
                "password": "Test12345",
                "captcha": "1234",
            },
            follow=True,
        )

        self.assertTrue(response.context["user"].is_authenticated)

    def test_wrong_password(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "arya",
                "password": "WrongPassword",
                "captcha": "1234",
            },
        )

        self.assertFalse(
            response.context["user"].is_authenticated
        )

    def test_username_not_exists(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "unknown",
                "password": "123456",
                "captcha": "1234",
            },
        )

        self.assertFalse(
            User.objects.filter(
                username="unknown"
            ).exists()
        )

    def test_wrong_captcha(self):
        session = self.client.session
        session["login_captcha"] = "5555"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "arya",
                "password": "Test12345",
                "captcha": "1234",
            },
        )

        self.assertFalse(
            response.context["user"].is_authenticated
        )

    def test_username_contains_space(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "ar ya",
                "password": "Test12345",
                "captcha": "1234",
            },
        )

        self.assertFalse(
            response.context["user"].is_authenticated
        )

    def test_password_contains_space(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "arya",
                "password": "Test 12345",
                "captcha": "1234",
            },
        )

        self.assertFalse(
            response.context["user"].is_authenticated
        )

    def test_login_captcha_removed_after_success(self):
        session = self.client.session
        session["login_captcha"] = "1234"
        session.save()

        self.client.post(
            reverse("accounts:login"),
            {
                "username": "arya",
                "password": "Test12345",
                "captcha": "1234",
            },
        )

        self.assertNotIn(
            "login_captcha",
            self.client.session
        )
        
        
        

class SignupViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        session = self.client.session
        session["register_captcha"] = "1234"
        session.save()


    @patch("accounts.views.send_otp")
    def test_signup_success_redirect_verify_email(self, mock_send):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "arya123",
                "email": "arya@test.com",
                "phone_number": "09123456789",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "captcha": "1234",
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:verify_email")
        )


        session = self.client.session

        self.assertEqual(
            session["signup_data"]["username"],
            "arya123"
        )

        mock_send.assert_called_once()


    def test_username_contains_space(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "arya test",
                "email": "test@test.com",
                "phone_number": "09123456789",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "captcha": "1234",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            User.objects.filter(
                username="arya test"
            ).exists()
        )


    def test_password_contains_space(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "arya123",
                "email": "test@test.com",
                "phone_number": "09123456789",
                "password1": "Strong Pass123!",
                "password2": "Strong Pass123!",
                "captcha": "1234",
            }
        )


        self.assertEqual(response.status_code,200)


    def test_wrong_captcha(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "arya123",
                "email": "test@test.com",
                "phone_number": "09123456789",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "captcha": "9999",
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


    def test_password_not_match(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"test@test.com",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"WrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)


    def test_username_less_than_4(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username":"abc",
                "email":"test@test.com",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )

        self.assertEqual(response.status_code,200)



    def test_invalid_email(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"invalid",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)



    def test_invalid_phone_number(self):

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"test@test.com",
                "phone_number":"12345",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)



    def test_duplicate_username(self):

        User.objects.create_user(
            username="arya123",
            password="Test12345"
        )


        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"test@test.com",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)



    def test_duplicate_email(self):

        User.objects.create_user(
            username="user1",
            email="test@test.com",
            password="Test12345"
        )


        response=self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"test@test.com",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)



    def test_duplicate_phone_number(self):

        user=User.objects.create_user(
            username="user1",
            password="Test12345"
        )

        Profile.objects.create(
            user=user,
            phone_number="09123456789"
        )


        response=self.client.post(
            reverse("accounts:signup"),
            {
                "username":"arya123",
                "email":"test@test.com",
                "phone_number":"09123456789",
                "password1":"StrongPass123!",
                "password2":"StrongPass123!",
                "captcha":"1234"
            }
        )


        self.assertEqual(response.status_code,200)
        


class VerifyEmailViewTest(TestCase):

    def setUp(self):
        self.signup_data = {
            "username": "arya123",
            "email": "arya@test.com",
            "password": "StrongPass123!",
            "phone_number": "09123456789",
        }

        session = self.client.session
        session["signup_data"] = self.signup_data
        session["otp"] = "123456"
        session["otp_time"] = int(time())
        session.save()


    def test_verify_email_success_creates_user_profile(self):

        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "otp": "123456"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:login_page")
        )


        user = User.objects.get(
            username="arya123"
        )

        self.assertEqual(
            user.email,
            "arya@test.com"
        )


        profile = Profile.objects.get(
            user=user
        )


        self.assertEqual(
            profile.phone_number,
            "09123456789"
        )



    def test_wrong_otp(self):

        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "otp":"999999"
            }
        )


        self.assertEqual(
            response.status_code,
            200
        )


        self.assertFalse(
            User.objects.filter(
                username="arya123"
            ).exists()
        )



    def test_expired_otp(self):

        session = self.client.session

        session["otp_time"] = int(time()) - 200

        session.save()


        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "otp":"123456"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:verify_email")
        )


        self.assertFalse(
            User.objects.filter(
                username="arya123"
            ).exists()
        )



    def test_missing_otp_session(self):

        session = self.client.session

        session.pop("otp_time")

        session.save()


        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "otp":"123456"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:login_page")
        )



    @patch("accounts.views.send_otp")
    def test_resend_otp_success(self, mock_send):

        session = self.client.session

        session["last_resend"] = int(time()) - 200

        session.save()


        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "resend":"1"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:verify_email")
        )


        mock_send.assert_called_once()



    def test_resend_before_time_limit(self):

        session = self.client.session

        session["last_resend"] = int(time())

        session.save()


        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "resend":"1"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:verify_email")
        )



    def test_resend_without_signup_session(self):

        session = self.client.session

        session.pop("signup_data")

        session.save()


        response = self.client.post(
            reverse("accounts:verify_email"),
            {
                "resend":"1"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:login_page")
        )



    def test_session_deleted_after_success(self):

        self.client.post(
            reverse("accounts:verify_email"),
            {
                "otp":"123456"
            }
        )


        session = self.client.session


        self.assertNotIn(
            "otp",
            session
        )


        self.assertNotIn(
            "otp_time",
            session
        )


        self.assertNotIn(
            "signup_data",
            session
        )
        
class ForgotPasswordTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="OldPassword123!"
        )

    # -------------------------
    # forgot_password_view
    # -------------------------

    def test_forgot_password_get(self):
        response = self.client.get(
            reverse("accounts:forgot_password")
        )

        self.assertEqual(response.status_code, 200)


    def test_forgot_password_logged_user_redirect(self):
        self.client.login(
            username="testuser",
            password="OldPassword123!"
        )

        response = self.client.get(
            reverse("accounts:forgot_password")
        )

        self.assertRedirects(
            response,
            reverse("notes:home")
        )


    @patch("accounts.views.send_otp")
    def test_valid_username_send_otp(self, mock_send):

        response = self.client.post(
            reverse("accounts:forgot_password"),
            {
                "username": "testuser"
            }
        )

        self.assertEqual(
            self.client.session["reset_username"],
            "testuser"
        )

        mock_send.assert_called_once()

        self.assertRedirects(
            response,
            reverse("accounts:verify_reset_password")
        )


    def test_invalid_username(self):

        response = self.client.post(
            reverse("accounts:forgot_password"),
            {
                "username": "unknown"
            }
        )

        self.assertRedirects(
            response,
            reverse("accounts:forgot_password")
        )


    # -------------------------
    # verify_reset_password_view
    # -------------------------

    def prepare_reset_session(self):

        session = self.client.session

        session["reset_username"] = "testuser"
        session["otp"] = "123456"
        session["otp_time"] = int(time())

        session.save()


    def test_correct_otp(self):

        self.prepare_reset_session()

        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "otp": "123456"
            }
        )

        session = self.client.session

        self.assertTrue(
            session["reset_verified"]
        )

        self.assertNotIn(
            "otp",
            session
        )

        self.assertNotIn(
            "otp_time",
            session
        )

        self.assertRedirects(
            response,
            reverse("accounts:new_password")
        )


    def test_wrong_otp(self):

        self.prepare_reset_session()

        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "otp": "999999"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Verification code is incorrect."
        )


    def test_missing_otp_time(self):

        session = self.client.session
        session["reset_username"] = "testuser"
        session.save()


        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "otp": "123456"
            }
        )

        self.assertRedirects(
            response,
            reverse("accounts:forgot_password")
        )


    def test_expired_otp(self):

        session = self.client.session

        session["otp"] = "123456"
        session["otp_time"] = int(time()) - 130
        session["reset_username"] = "testuser"

        session.save()


        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "otp": "123456"
            }
        )

        self.assertRedirects(
            response,
            reverse("accounts:verify_reset_password")
        )

        self.assertNotIn(
            "otp",
            self.client.session
        )


    @patch("accounts.views.send_otp")
    def test_resend_success(self, mock_send):

        session = self.client.session

        session["reset_username"] = "testuser"
        session["last_resend"] = int(time()) - 130

        session.save()


        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "resend": "1"
            }
        )

        mock_send.assert_called_once()

        self.assertRedirects(
            response,
            reverse("accounts:verify_reset_password")
        )


    def test_resend_before_time(self):

        session = self.client.session

        session["reset_username"] = "testuser"
        session["last_resend"] = int(time())

        session.save()


        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "resend": "1"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:verify_reset_password")
        )


    def test_resend_without_username(self):

        response = self.client.post(
            reverse("accounts:verify_reset_password"),
            {
                "resend": "1"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:forgot_password")
        )


    def prepare_verified_session(self):

        session = self.client.session

        session["reset_verified"] = True
        session["reset_username"] = "testuser"

        session.save()



    def test_new_password_get_without_verify(self):

        response = self.client.get(
            reverse("accounts:new_password")
        )


        self.assertRedirects(
            response,
            reverse("accounts:forgot_password")
        )


    def test_new_password_success(self):

        self.prepare_verified_session()


        response = self.client.post(
            reverse("accounts:new_password"),
            {
                "password1": "NewPassword123!",
                "password2": "NewPassword123!"
            }
        )


        user = User.objects.get(
            username="testuser"
        )

        self.assertTrue(
            user.check_password("NewPassword123!")
        )


        session = self.client.session


        self.assertNotIn(
            "reset_username",
            session
        )

        self.assertNotIn(
            "reset_verified",
            session
        )


        self.assertTrue(
            session["show_login"]
        )


        self.assertRedirects(
            response,
            reverse("accounts:login_page")
        )


    def test_password_not_match(self):

        self.prepare_verified_session()


        response = self.client.post(
            reverse("accounts:new_password"),
            {
                "password1":"Password123!",
                "password2":"Different123!"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:new_password")
        )


    def test_password_has_space(self):

        self.prepare_verified_session()


        response = self.client.post(
            reverse("accounts:new_password"),
            {
                "password1":"New Pass123!",
                "password2":"New Pass123!"
            }
        )


        self.assertRedirects(
            response,
            reverse("accounts:new_password")
        )           



class LoginPageViewTest(TestCase):

    def test_login_page_get(self):

        response = self.client.get(
            reverse("accounts:login_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "login_captcha",
            self.client.session
        )

        self.assertIn(
            "register_captcha",
            self.client.session
        )


    def test_authenticated_user_redirect(self):

        user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )

        self.client.login(
            username="arya",
            password="Test12345"
        )

        response = self.client.get(
            reverse("accounts:login_page")
        )

        self.assertRedirects(
            response,
            reverse("notes:home")
        )


    def test_show_login_removed_from_session(self):

        session = self.client.session

        session["show_login"] = True

        session.save()


        response = self.client.get(
            reverse("accounts:login_page")
        )


        self.assertFalse(
            self.client.session.get(
                "show_login",
                False
            )
        )       
        

 
        
class LogoutViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="arya",
            password="Test12345"
        )


    def test_logout_success(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )

        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("notes:home")
        )


        response = self.client.get(
            reverse("accounts:login_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_user_logged_out(self):

        self.client.login(
            username="arya",
            password="Test12345"
        )

        self.client.get(
            reverse("accounts:logout")
        )


        response = self.client.get(
            reverse("accounts:login_page")
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )


    def test_logout_without_login(self):

        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            "/login/?next=/logout"
        )       
        
        
        
class AccountsURLTest(TestCase):

    def test_login_url_exists(self):
        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertEqual(
            response.status_code,
            302
        )


    def test_signup_url_exists(self):
        response = self.client.get(
            reverse("accounts:signup")
        )

        self.assertEqual(
            response.status_code,
            302
        )


    def test_login_page_url_exists(self):
        response = self.client.get(
            reverse("accounts:login_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_verify_email_url_exists(self):
        response = self.client.get(
            reverse("accounts:verify_email")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_forgot_password_url_exists(self):
        response = self.client.get(
            reverse("accounts:forgot_password")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_verify_reset_password_url_exists(self):

        response = self.client.get(
            reverse("accounts:verify_reset_password")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_new_password_url_exists(self):

        response = self.client.get(
            reverse("accounts:new_password")
        )

        self.assertEqual(
            response.status_code,
            302
        ) 