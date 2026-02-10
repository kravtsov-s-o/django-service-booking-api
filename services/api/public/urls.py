from rest_framework.routers import DefaultRouter

from services.api.public.views import ServicesViewSet

router = DefaultRouter()
router.register("services", ServicesViewSet, basename="services")

urlpatterns = router.urls
