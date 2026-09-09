from django.urls import path
from .views import OfficerListView,InvitationView,OfficerActionView
urlpatterns=[path("",OfficerListView.as_view()),path("invite/",InvitationView.as_view()),path("<int:pk>/<str:action>/",OfficerActionView.as_view())]
