import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")
SECRET_KEY=os.getenv("SECRET_KEY","unsafe-development-key")
DEBUG=os.getenv("DEBUG","True").lower()=="true"
ALLOWED_HOSTS=[h.strip() for h in os.getenv("ALLOWED_HOSTS","localhost,127.0.0.1").split(",") if h.strip()]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","corsheaders","rest_framework","django_filters","apps.core","apps.audit","apps.history","apps.settings_app","apps.ai","apps.officers","apps.verification"]
MIDDLEWARE=["corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":dj_database_url.config(default=f"sqlite:///{BASE_DIR/'db.sqlite3'}",conn_max_age=600,conn_health_checks=True)}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE="en-us"; TIME_ZONE="UTC"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"; MEDIA_ROOT=BASE_DIR/"private_uploads"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
FRONTEND_URL=os.getenv("FRONTEND_URL","http://localhost:3000,http://127.0.0.1:3000")
CORS_ALLOWED_ORIGINS=[u.strip() for u in FRONTEND_URL.split(",") if u.strip()]
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=CORS_ALLOWED_ORIGINS
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["apps.core.authentication.OfficerSessionAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],"DEFAULT_PAGINATION_CLASS":"apps.core.pagination.StandardPagination","PAGE_SIZE":20,"DEFAULT_FILTER_BACKENDS":["django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"],"EXCEPTION_HANDLER":"apps.core.exceptions.api_exception_handler","DEFAULT_THROTTLE_RATES":{"officer_login":"5/min"}}
SECURE_SSL_REDIRECT=not DEBUG; SESSION_COOKIE_SECURE=not DEBUG; SESSION_COOKIE_HTTPONLY=True; SESSION_COOKIE_SAMESITE="Lax"; CSRF_COOKIE_SECURE=not DEBUG; CSRF_COOKIE_HTTPONLY=False; SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https"); X_FRAME_OPTIONS="DENY"; SECURE_CONTENT_TYPE_NOSNIFF=True; SECURE_REFERRER_POLICY="same-origin"
