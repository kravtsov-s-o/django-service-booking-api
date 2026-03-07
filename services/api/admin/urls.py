from core.api.routers import build_router
from services.api.admin.views import (
    AdminServicesViewSet,
    AdminSpecialistServicesViewSet,
)

urlpatterns = build_router(
    ("services", AdminServicesViewSet, "admin-services"),
    (
        "specialist-services",
        AdminSpecialistServicesViewSet,
        "admin-specialist-services",
    ),
)
