from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import OfficerInvitation, OfficerProfile


class OfficerAuthenticationTests(TestCase):
    def setUp(self):
        self.admin=get_user_model().objects.create_user(username="admin@example.gov",email="admin@example.gov",password="SecurePassword123!")
        OfficerProfile.objects.create(user=self.admin,role=OfficerProfile.Role.SUPER_ADMIN,is_active=True)
        self.invitation=OfficerInvitation.objects.create(email="officer@example.gov",created_by=self.admin)
        self.client=APIClient()

    def test_registration_login_and_authenticated_profile(self):
        registered=self.client.post("/api/auth/register/",{"token":self.invitation.token,"email":"officer@example.gov","password":"AnotherSecure123!","password_confirmation":"AnotherSecure123!"},format="json")
        self.assertEqual(registered.status_code,201)
        self.assertTrue(registered.data["success"])

        logged_in=self.client.post("/api/auth/login/",{"email":"officer@example.gov","password":"AnotherSecure123!"},format="json")
        self.assertEqual(logged_in.status_code,200)
        self.assertTrue(logged_in.data["success"])

        profile=self.client.get("/api/auth/me/")
        self.assertEqual(profile.status_code,200)
        self.assertEqual(profile.data["data"]["email"],"officer@example.gov")

    def test_invalid_login_and_mismatched_registration_are_explained(self):
        invalid_login=self.client.post("/api/auth/login/",{"email":"missing@example.gov","password":"WrongPassword123!"},format="json")
        self.assertEqual(invalid_login.status_code,401)
        self.assertEqual(invalid_login.data["error"]["code"],"INVALID_LOGIN")

        mismatched=self.client.post("/api/auth/register/",{"token":self.invitation.token,"email":"officer@example.gov","password":"AnotherSecure123!","password_confirmation":"DifferentPassword123!"},format="json")
        self.assertEqual(mismatched.status_code,400)
        self.assertIn("Passwords do not match",str(mismatched.data))

    def test_registration_rejects_an_email_not_authorized_by_the_invitation(self):
        response=self.client.post("/api/auth/register/",{"token":self.invitation.token,"email":"other@example.gov","password":"AnotherSecure123!","password_confirmation":"AnotherSecure123!"},format="json")
        self.assertEqual(response.status_code,422)
        self.assertEqual(response.data["error"]["code"],"INVALID_INVITATION")
