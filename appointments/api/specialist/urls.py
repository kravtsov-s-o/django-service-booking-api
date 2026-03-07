from appointments.api.specialist.views import SpecialistServiceRecordViewSet
from core.api.routers import build_router

urlpatterns = build_router(
    ("schedule", SpecialistServiceRecordViewSet, "specialist-schedule")
)
