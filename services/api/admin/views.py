from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from services.api.admin.serializers import (
    AdminServiceSerializer,
    AdminSpecialistServiceSerializer,
)
from services.models import Service, SpecialistService
from users.api.admin.permissions import IsAdminUserRole


@extend_schema(tags=["Admin: Services"],
    summary="Admin service management")
class AdminServicesViewSet(viewsets.ModelViewSet):
    """
    Admin service management.

    Provides CRUD operations for services.

    Deleting a service archives it by setting is_active=False.
    """
    queryset = Service.objects.all()
    serializer_class = AdminServiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()

        service.is_active = False
        service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Admin: Specialist Services"])
class AdminSpecialistServicesViewSet(viewsets.ModelViewSet):
    """
    Admin management of specialist service assignments.

    Allows administrators to assign services to specialists
    and configure payout rules.
    """
    queryset = SpecialistService.objects.select_related(
        "specialist__user", "service"
    ).filter(is_active=True)
    serializer_class = AdminSpecialistServiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)

    def destroy(self, request, *args, **kwargs):
        specialist_service = self.get_object()

        specialist_service.is_active = False
        specialist_service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
