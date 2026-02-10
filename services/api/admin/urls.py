from rest_framework.routers import DefaultRouter

from services.api.admin.views import AdminServicesViewSet

router = DefaultRouter()
router.register("services", AdminServicesViewSet, basename="admin-services")

urlpatterns = router.urls