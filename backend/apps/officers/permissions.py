from rest_framework.permissions import BasePermission
class OfficerRequired(BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active and hasattr(request.user,"officer_profile") and request.user.officer_profile.is_active)
class SuperAdminRequired(OfficerRequired):
    def has_permission(self,request,view):
        return super().has_permission(request,view) and request.user.officer_profile.role=="SUPER_ADMIN"
