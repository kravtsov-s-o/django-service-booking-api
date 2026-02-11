from rest_framework.routers import DefaultRouter

from services.api.admin.views import (
    AdminServicesViewSet,
    AdminSpecialistServicesViewSet,
)

router = DefaultRouter()
router.register("services", AdminServicesViewSet, basename="admin-services")
router.register(
    "specialist-services",
    AdminSpecialistServicesViewSet,
    basename="admin-specialist-services",
)

urlpatterns = router.urls
