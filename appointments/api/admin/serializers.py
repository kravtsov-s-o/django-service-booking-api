from rest_framework import serializers

from appointments.api.base.serializers import BaseServiceRecordSerializer
from appointments.models import ServiceRecord


class AdminServiceRecordSerializer(BaseServiceRecordSerializer):
    """
    Serializer for managing service appointments in the admin API.

    Provides full visibility of appointments including:
    - client and specialist participants
    - financial data recorded after service completion

    Booking validation rules are inherited from BaseServiceRecordSerializer.
    """

    client_name = serializers.CharField(
        source="client.user",
        read_only=True,
    )

    specialist_name = serializers.CharField(
        source="specialist.user",
        read_only=True,
    )

    class Meta(BaseServiceRecordSerializer.Meta):
        model = ServiceRecord
        fields = BaseServiceRecordSerializer.Meta.fields + (
            "client",
            "client_name",
            "specialist",
            "specialist_name",
            "completed_at",
            "service_price",
            "specialist_payout",
        )
        read_only_fields = BaseServiceRecordSerializer.Meta.read_only_fields + (
            "completed_at",
            "service_price",
            "specialist_payout",
        )

    def validate(self, attrs):
        specialist = attrs.get("specialist", getattr(self.instance, "specialist", None))
        service = attrs.get("service", getattr(self.instance, "service", None))
        scheduled_at = attrs.get("scheduled_at", getattr(self.instance, "scheduled_at", None))

        self.validate_booking(specialist, service, scheduled_at)

        return attrs
