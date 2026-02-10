from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from services.api.admin.serializers import (
    AdminServiceSerializer,
    AdminSpecialistServiceSerializer,
)
from services.models import Service, SpecialistService
from users.api.admin.permissions import IsAdminUserRole


class AdminServicesViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = AdminServiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()

        service.is_active = False
        service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminSpecialistServicesViewSet(viewsets.ModelViewSet):
    queryset = SpecialistService.objects.filter(is_active=True)
    serializer_class = AdminSpecialistServiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)

    def destroy(self, request, *args, **kwargs):
        specialist_service = self.get_object()

        specialist_service.is_active = False
        specialist_service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
