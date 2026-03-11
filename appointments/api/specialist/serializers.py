from rest_framework import serializers

from appointments.api.base.serializers import BaseServiceRecordSerializer
from appointments.models import ServiceRecord


class SpecialistServiceRecordSerializer(BaseServiceRecordSerializer):
    """
    Serializer for specialist appointment operations.

    Specialists can manage appointments with clients.
    Includes client information for schedule visibility.
    """

    client_name = serializers.CharField(
        source="client.user",
        read_only=True,
    )

    class Meta(BaseServiceRecordSerializer.Meta):
        model = ServiceRecord
        fields = BaseServiceRecordSerializer.Meta.fields + ("client", "client_name")

    def validate(self, attrs):
        specialist = self.context["request"].user.specialist_profile
        service = attrs["service"]
        scheduled_at = attrs["scheduled_at"]

        self.validate_booking(specialist, service, scheduled_at)

        return attrs
