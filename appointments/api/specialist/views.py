from rest_framework.permissions import IsAuthenticated

from appointments.api.base.views import BaseServiceRecordViewSet
from appointments.api.specialist.serializers import SpecialistServiceRecordSerializer
from users.api.permissions import IsSpecialistUser


class SpecialistServiceRecordViewSet(BaseServiceRecordViewSet):
    serializer_class = SpecialistServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsSpecialistUser)

    lookup_user_field = "specialist"
    select_related_fields = ("service", "specialist__user", "client__user")

    def get_profile(self):
        return self.request.user.specialist_profile

    # @action(detail=True, methods=["post"], url_path="complete")
    # def complete(self, request, pk=None):
    #     appointment = self.get_object()
    #
    #     if appointment.status != appointment.Status.PLANNED:
    #         return Response({"detail": "Only planned appointments can be Completed."},
    #                         status=status.HTTP_400_BAD_REQUEST,
    #                         )
    #
    #     appointment.status = ServiceRecord.Status.COMPLETED
    #     appointment.save(update_fields=["status", "updated_at"])
    #
    #     return Response(status=status.HTTP_200_OK)
