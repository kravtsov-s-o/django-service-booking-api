from core.api.routers import build_router
from users.api.admin.views import AdminUserViewSet

urlpatterns = build_router(("users", AdminUserViewSet, "admin-users"))
