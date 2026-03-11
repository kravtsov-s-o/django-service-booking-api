from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.api.admin.serializers import AdminServiceRecordSerializer
from appointments.api.base.views import AdminSpecialistServiceRecordViewSet
from appointments.services.refund import refund
from users.api.admin.permissions import IsAdminUserRole


@extend_schema(tags=["Admin: Appointments"])
class AdminServiceRecordViewSet(
    AdminSpecialistServiceRecordViewSet, viewsets.ModelViewSet
):
    """
    Admin appointment management.

    Provides full CRUD access to service appointments.

    Additional operations:
    - cancel appointment
    - complete appointment
    - refund completed services

    Permissions:
    Admin users only.
    """
    serializer_class = AdminServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsAdminUserRole)

    select_related_fields = ("service", "specialist__user", "client__user")

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        """
        Refund the client for a completed service.

        Creates a wallet transaction that returns the service amount
        to the client's wallet.
        """
        appointment = self.get_object()

        try:
            refund(appointment)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
