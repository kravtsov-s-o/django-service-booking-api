from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.api.admin.serializers import AdminServiceRecordSerializer
from appointments.api.base.views import AdminSpecialistServiceRecordViewSet
from users.api.admin.permissions import IsAdminUserRole


class AdminServiceRecordViewSet(AdminSpecialistServiceRecordViewSet, viewsets.ModelViewSet):
    serializer_class = AdminServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsAdminUserRole)

    select_related_fields = ("service", "specialist__user", "client__user")

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        # appointment = self.get_object()

        try:
            pass
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
