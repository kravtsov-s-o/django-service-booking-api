from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from appointments.models import ServiceRecord


class BaseServiceRecordViewSet(GenericViewSet):
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
        appointment = self.get_object()

        try:
            appointment.transition(ServiceRecord.Status.CANCELLED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class UserScopedServiceRecordViewSet(
    BaseServiceRecordViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    lookup_user_field = None

    def get_profile(self):
        raise NotImplementedError()

    def perform_create(self, serializer):
        serializer.save(**{self.lookup_user_field: self.get_profile()})
