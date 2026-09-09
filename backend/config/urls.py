from django.contrib import admin
from django.urls import include,path
urlpatterns=[path("admin/",admin.site.urls),path("api/",include("apps.core.urls")),path("api/auth/",include("apps.officers.auth_urls")),path("api/officers/",include("apps.officers.urls")),path("api/verification/",include("apps.verification.urls")),path("api/audit/",include("apps.audit.urls")),path("api/history/",include("apps.history.urls")),path("api/settings/",include("apps.settings_app.urls")),path("api/ai/",include("apps.ai.urls"))]
