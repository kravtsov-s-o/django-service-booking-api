from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.api.base.views import UserScopedServiceRecordViewSet
from appointments.api.specialist.serializers import SpecialistServiceRecordSerializer
from appointments.models import ServiceRecord
from users.api.permissions import IsSpecialistUser


class SpecialistServiceRecordViewSet(UserScopedServiceRecordViewSet):
    serializer_class = SpecialistServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsSpecialistUser)

    lookup_user_field = "specialist"
    select_related_fields = ("service", "specialist__user", "client__user")

    def get_profile(self):
        return self.request.user.specialist_profile

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        appointment = self.get_object()

        try:
            appointment.transition(ServiceRecord.Status.COMPLETED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
