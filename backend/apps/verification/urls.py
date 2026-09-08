from django.urls import path
from .views import VerificationListCreate,VerificationDetail,UploadView,AuditLogView,ProviderStatusView
urlpatterns=[path("",VerificationListCreate.as_view()),path("<uuid:pk>/",VerificationDetail.as_view()),path("<uuid:pk>/upload/",UploadView.as_view()),path("audit/",AuditLogView.as_view()),path("providers/",ProviderStatusView.as_view())]
