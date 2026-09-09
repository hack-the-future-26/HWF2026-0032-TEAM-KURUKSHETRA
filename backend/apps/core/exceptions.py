from rest_framework.views import exception_handler
from rest_framework.response import Response
def api_exception_handler(exc,context):
 response=exception_handler(exc,context)
 if response: response.data={"success":False,"error":{"message":str(exc.detail),"code":getattr(exc,"default_code","REQUEST_ERROR")}}
 return response
