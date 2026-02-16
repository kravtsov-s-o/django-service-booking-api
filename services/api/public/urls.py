from core.api.routers import build_router
from services.api.public.views import ServicesViewSet

urlpatterns = build_router(("services", ServicesViewSet, "public-services"))
