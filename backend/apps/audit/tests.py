from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from apps.officers.models import OfficerProfile

class AuthorizationTests(APITestCase):
 def setUp(self):
  self.admin=User.objects.create_user(username="admin@gov.test",email="admin@gov.test",password="StrongPassword123!")
  OfficerProfile.objects.create(user=self.admin,role="SUPER_ADMIN",is_active=True)
  self.officer=User.objects.create_user(username="officer@gov.test",email="officer@gov.test",password="StrongPassword123!")
  OfficerProfile.objects.create(user=self.officer,role="OFFICER",is_active=True)
 def test_protected_api_rejects_anonymous_requests(self): self.assertEqual(self.client.get("/api/audit/").status_code,401)
 def test_officer_cannot_manage_officers(self):
  self.client.force_login(self.officer);self.assertEqual(self.client.get("/api/officers/").status_code,403)
 def test_admin_can_invite_officer(self):
  self.client.force_login(self.admin);response=self.client.post("/api/officers/invite/",{"email":"new@gov.test"},format="json");self.assertEqual(response.status_code,201)
 def test_officer_creates_manual_review_verification(self):
  self.client.force_login(self.officer);response=self.client.post("/api/verification/",{"bidder_name":"Acme Pvt Ltd","document_type":"GST"},format="json");self.assertEqual(response.status_code,201)
