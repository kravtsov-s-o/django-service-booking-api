from appointments.api.admin.views import AdminServiceRecordViewSet
from core.api.routers import build_router

urlpatterns = build_router(
    ("appointments", AdminServiceRecordViewSet, "admin-appointments")
)
