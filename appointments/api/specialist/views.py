from rest_framework.permissions import IsAuthenticated

from appointments.api.base.views import (
    AdminSpecialistServiceRecordViewSet,
    UserScopedServiceRecordViewSet,
)
from appointments.api.specialist.serializers import SpecialistServiceRecordSerializer
from users.api.permissions import IsSpecialistUser


class SpecialistServiceRecordViewSet(
    AdminSpecialistServiceRecordViewSet, UserScopedServiceRecordViewSet
):
    serializer_class = SpecialistServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsSpecialistUser)

    lookup_user_field = "specialist"
    select_related_fields = ("service", "specialist__user", "client__user")

    def get_profile(self):
        return self.request.user.specialist_profile
