from rest_framework.routers import DefaultRouter
from .views import HistoryViewSet
router=DefaultRouter();router.register("",HistoryViewSet,basename="history");urlpatterns=router.urls
