from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.api.admin.permissions import IsAdminUserRole
from users.api.admin.serializers import (
    AdminSetPasswordSerializer,
    AdminUserCreateSerializer,
    AdminUserUpdateSerializer,
)

User = get_user_model()


@extend_schema(tags=["Admin: Users"])
class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin user management.

    Provides CRUD operations for managing users in the system.\n
    DELETE deactivates the user by setting is_active=False.

    Endpoints:
    - GET /admin/users/        — list users
    - POST /admin/users/       — create user
    - GET /admin/users/{id}/   — retrieve user
    - PATCH /admin/users/{id}/ — update user
    - DELETE /admin/users/{id}/ — deactivate user

    Special actions:
    - POST /admin/users/{id}/set-password/ — reset user password.

    Permissions:
    Admin users only.
    """

    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)
    queryset = User.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return AdminUserCreateSerializer

        return AdminUserUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Reset user password",
        description="Set a new password for the specified user.",
    )
    @action(detail=True, methods=["post"], url_path="set-password")
    def set_password(self, request, pk=None):
        user = self.get_object()

        serializer = AdminSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response(
            {"detail": "Password has been reset."}, status=status.HTTP_200_OK
        )
