from rest_framework.authentication import SessionAuthentication
class OfficerSessionAuthentication(SessionAuthentication):
    """Return 401 rather than 403 when no session credential exists."""
    def authenticate_header(self,request): return "Session"
