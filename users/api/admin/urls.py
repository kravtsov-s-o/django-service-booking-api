from rest_framework.routers import DefaultRouter

from users.api.admin.views import AdminUserViewSet

router = DefaultRouter()
router.register("users", AdminUserViewSet, basename="admin-users")

urlpatterns = router.urls
