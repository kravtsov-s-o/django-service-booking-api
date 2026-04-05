from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from appointments.api.base.views import UserScopedServiceRecordViewSet
from appointments.api.client.serializer import ClientServiceRecordSerializer
from users.api.permissions import IsClientUser


# Create your views here.
@extend_schema(tags=["Profile: Client Appointments"])
class ClientServiceRecordViewSet(UserScopedServiceRecordViewSet):
    """
    Client appointment management.

    Allows clients to:
    - create service appointments
    - view their appointment history
    - cancel scheduled appointments

    Permissions:
    Client users only.
    """

    serializer_class = ClientServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsClientUser)

    lookup_user_field = "client"
    select_related_fields = ("service", "specialist__user")

    def get_profile(self):
        return self.request.user.client_profile
