from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.api.base.views import UserScopedServiceRecordViewSet, AdminSpecialistServiceRecordViewSet
from appointments.api.specialist.serializers import SpecialistServiceRecordSerializer
from users.api.permissions import IsSpecialistUser


class SpecialistServiceRecordViewSet(AdminSpecialistServiceRecordViewSet, UserScopedServiceRecordViewSet):
    serializer_class = SpecialistServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsSpecialistUser)

    lookup_user_field = "specialist"
    select_related_fields = ("service", "specialist__user", "client__user")

    def get_profile(self):
        return self.request.user.specialist_profile
