from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from services.api.admin.serializers import AdminServiceSerializer
from services.models import Service
from users.api.admin.permissions import IsAdminUserRole


class AdminServicesViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = AdminServiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUserRole)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()

        service.is_active = False
        service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
