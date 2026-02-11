from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from appointments.models import ServiceRecord
from services.models import SpecialistService


class ClientServiceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = (
            "id",
            "specialist",
            "service",
            "scheduled_at",
            "status",
        )
        read_only_fields = ("id", "status")

    def validate(self, attrs):
        specialist = attrs["specialist"]
        service = attrs["service"]
        scheduled_at = attrs["scheduled_at"]

        if not service.is_active:
            raise serializers.ValidationError({"service": "Service is not available."})

        if not specialist.user.is_active:
            raise serializers.ValidationError(
                {"specialist": "Specialist is not active."}
            )

        if not SpecialistService.objects.filter(
                specialist=specialist,
                service=service,
                is_active=True,
        ).exists():
            raise serializers.ValidationError(
                "Selected specialist does not provide this service."
            )

        if ServiceRecord.objects.filter(
                specialist=specialist,
                scheduled_at=scheduled_at,
                status=ServiceRecord.Status.PLANNED,
        ):
            raise serializers.ValidationError(
                {"scheduled_at": "This time slot is already booked."}
            )

        return attrs

    def validate_scheduled_at(self, value):
        if value <= timezone.now() + timedelta(hours=1):
            raise serializers.ValidationError(
                "Appointment must be scheduled in the future."
            )

        return value
