from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class StandardPagination(PageNumberPagination):
 page_size_query_param="page_size"; max_page_size=100
 def get_paginated_response(self,data): return Response({"success":True,"data":{"results":data,"count":self.page.paginator.count,"page":self.page.number,"total_pages":self.page.paginator.num_pages}})
