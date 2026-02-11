from rest_framework.routers import DefaultRouter

from appointments.api.client.views import ClientServiceRecordViewSet

router = DefaultRouter()
router.register(
    "appointments", ClientServiceRecordViewSet, basename="client-appointments"
)
urlpatterns = router.urls
