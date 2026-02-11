from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.api.admin.permissions import IsAdminUserRole
from users.api.admin.serializers import (
    AdminUserCreateSerializer,
    AdminUserUpdateSerializer,
    AdminSetPasswordSerializer,
)

User = get_user_model()


class AdminUserViewSet(viewsets.ModelViewSet):
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
