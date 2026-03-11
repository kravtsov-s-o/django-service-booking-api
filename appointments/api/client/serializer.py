from rest_framework import serializers

from appointments.api.base.serializers import BaseServiceRecordSerializer
from appointments.models import ServiceRecord


class ClientServiceRecordSerializer(BaseServiceRecordSerializer):
    """
    Serializer for client appointment operations.

    Extends BaseServiceRecordSerializer and adds
    client-specific fields such as the selected specialist.
    """

    specialist_name = serializers.CharField(
        source="specialist.user",
        read_only=True,
    )

    class Meta(BaseServiceRecordSerializer.Meta):
        model = ServiceRecord
        fields = BaseServiceRecordSerializer.Meta.fields + (
            "specialist",
            "specialist_name",
        )

    def validate(self, attrs):
        specialist = attrs["specialist"]
        service = attrs["service"]
        scheduled_at = attrs["scheduled_at"]

        self.validate_booking(specialist, service, scheduled_at)

        return attrs
