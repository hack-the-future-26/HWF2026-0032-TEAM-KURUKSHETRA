import os
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth import get_user_model
from apps.officers.models import OfficerProfile
class Command(BaseCommand):
 help="Creates or promotes the official administrator from environment variables."
 def handle(self,*args,**kwargs):
  email=os.getenv("INITIAL_ADMIN_EMAIL","saivarshak14@gmail.com").lower();password=os.getenv("INITIAL_ADMIN_PASSWORD")
  if not password: raise CommandError("Set INITIAL_ADMIN_PASSWORD before seeding the official administrator.")
  User=get_user_model();user,created=User.objects.get_or_create(email=email,defaults={"username":email,"is_active":True})
  if not created and not user.check_password(password):user.set_password(password)
  user.username=email;user.is_active=True;user.is_staff=True;user.is_superuser=True;user.save()
  profile,_=OfficerProfile.objects.get_or_create(user=user);profile.role=OfficerProfile.Role.SUPER_ADMIN;profile.is_active=True;profile.save()
  self.stdout.write(self.style.SUCCESS("Official administrator is ready."))
