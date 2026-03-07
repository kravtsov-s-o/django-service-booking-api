from appointments.api.client.views import ClientServiceRecordViewSet
from core.api.routers import build_router

urlpatterns = build_router(
    ("appointments", ClientServiceRecordViewSet, "client-appointments")
)
