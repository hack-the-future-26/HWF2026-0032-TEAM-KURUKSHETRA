from django.utils import timezone
from .models import VerificationResult
from .providers import ManualVerificationProvider
def run_verification(request):
 result=ManualVerificationProvider().verify({"document_type":request.document_type})
 request.status=result["status"];request.source=result["source"];request.requires_manual_review=result["requires_manual_review"];request.save(update_fields=["status","source","requires_manual_review","updated_at"])
 VerificationResult.objects.update_or_create(request=request,defaults={"confidence":result["confidence"],"details":result["details"],"errors":result["errors"],"verified_at":timezone.now() if result["status"]=="VERIFIED" else None})
 return request
