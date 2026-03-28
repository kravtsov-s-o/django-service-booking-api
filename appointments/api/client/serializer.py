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
        specialist = attrs.get("specialist", getattr(self.instance, "specialist", None))
        service = attrs.get("service", getattr(self.instance, "service", None))
        scheduled_at = attrs.get("scheduled_at", getattr(self.instance, "scheduled_at", None))

        self.validate_booking(specialist, service, scheduled_at)

        return attrs
