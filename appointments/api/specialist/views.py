from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from appointments.api.base.views import (
    AdminSpecialistServiceRecordViewSet,
    UserScopedServiceRecordViewSet,
)
from appointments.api.specialist.serializers import SpecialistServiceRecordSerializer
from users.api.permissions import IsSpecialistUser


@extend_schema(tags=["ЗкщашдуЖ Specialist Schedule"])
class SpecialistServiceRecordViewSet(
    AdminSpecialistServiceRecordViewSet, UserScopedServiceRecordViewSet
):
    """
    Specialist appointment management.

    Allows specialists to:
    - create appointments for clients
    - view their schedule
    - cancel appointments
    - complete services
    """
    serializer_class = SpecialistServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsSpecialistUser)

    lookup_user_field = "specialist"
    select_related_fields = ("service", "specialist__user", "client__user")

    def get_profile(self):
        return self.request.user.specialist_profile
