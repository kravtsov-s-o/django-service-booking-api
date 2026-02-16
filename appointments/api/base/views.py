from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from appointments.models import ServiceRecord


class BaseServiceRecordViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    permission_classes = (IsAuthenticated,)

    lookup_user_field = None
    select_related_fields = ("service",)

    def get_profile(self):
        raise NotImplementedError()

    def get_queryset(self):
        profile = self.get_profile()

        return (
            ServiceRecord.objects.filter(**{self.lookup_user_field: profile})
            .select_related(*self.select_related_fields)
            .order_by("-scheduled_at")
        )

    def perform_create(self, serializer):
        serializer.save(**{self.lookup_user_field: self.get_profile()})

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != appointment.Status.PLANNED:
            return Response(
                {"detail": "Only planned appointments can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = ServiceRecord.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])

        return Response(status=status.HTTP_200_OK)
