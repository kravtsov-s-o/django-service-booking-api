from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from appointments.api.client.serializer import ClientServiceRecordSerializer
from appointments.models import ServiceRecord
from users.api.permissions import IsClientUser


# Create your views here.
class ClientServiceRecordViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    serializer_class = ClientServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsClientUser)

    def get_queryset(self):
        return (
            ServiceRecord.objects.filter(client=self.request.user.client_profile)
            .select_related("service", "specialist__user")
            .order_by("-scheduled_at")
        )

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client_profile)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != appointment.Status.PLANNED:
            return Response(
                {"detail": "Only planned appointments can be cancelled."}
            )

        appointment.status = ServiceRecord.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])

        return Response(status=status.HTTP_200_OK)
