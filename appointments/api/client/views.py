from rest_framework.permissions import IsAuthenticated

from appointments.api.base.views import UserScopedServiceRecordViewSet
from appointments.api.client.serializer import ClientServiceRecordSerializer
from users.api.permissions import IsClientUser


# Create your views here.
class ClientServiceRecordViewSet(UserScopedServiceRecordViewSet):
    serializer_class = ClientServiceRecordSerializer
    permission_classes = (IsAuthenticated, IsClientUser)

    lookup_user_field = "client"
    select_related_fields = ("service", "specialist__user")

    def get_profile(self):
        return self.request.user.client_profile
