from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from appointments.models import ServiceRecord
from appointments.services.completion import complete_service_record


class BaseServiceRecordViewSet(GenericViewSet):
    """
    Base viewset for service appointment operations.

    Provides shared behaviour for appointment endpoints:
    - common queryset configuration
    - appointment cancellation

    Specialized viewsets extend this class and add
    role-specific logic (client, specialist, admin).
    """
    queryset = ServiceRecord.objects.all()
    select_related_fields = ("service",)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(*self.select_related_fields)
            .order_by("-scheduled_at")
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        """
        Cancel an appointment.

        Allowed only if the appointment can transition to CANCELLED status.
        """
        appointment = self.get_object()

        try:
            appointment.transition(ServiceRecord.Status.CANCELLED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class AdminSpecialistServiceRecordViewSet(BaseServiceRecordViewSet):
    """
    Shared viewset for specialist and admin appointment completion.

    Provides the `complete` action used by both specialist
    and admin endpoints to finalize a service appointment.
    """
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        Complete a service appointment.

        Triggers the business workflow that:
        - charges the client's wallet
        - records financial snapshots
        - transitions the appointment to COMPLETED
        """
        appointment = self.get_object()

        try:
            complete_service_record(appointment)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class UserScopedServiceRecordViewSet(
    BaseServiceRecordViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    """
    Base viewset for user-scoped appointment endpoints.

    Restricts queries and creation to the current user's profile.
    Used for client and specialist appointment APIs.
    """
    lookup_user_field = None

    def get_profile(self):
        raise NotImplementedError()

    def perform_create(self, serializer):
        serializer.save(**{self.lookup_user_field: self.get_profile()})
