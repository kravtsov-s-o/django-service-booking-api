from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from appointments.models import ServiceRecord
from services.models import SpecialistService


class BaseServiceRecordSerializer(serializers.ModelSerializer):
    """
    Contains booking business rules.
    Client/Specialist serializers only provide participants.
    """

    service_title = serializers.CharField(
        source="service.title",
        read_only=True,
    )

    class Meta:
        model = ServiceRecord
        fields = (
            "id",
            "service",
            "service_title",
            "scheduled_at",
            "status",
        )
        read_only_fields = ("id", "status")

    def validate_scheduled_at(self, value):
        if value <= timezone.now() + timedelta(hours=1):
            raise serializers.ValidationError(
                "Appointment must be scheduled in the future."
            )

        return value

    def validate_booking(self, specialist, service, scheduled_at):
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
                {"service": "Selected specialist does not provide this service."}
            )

        if ServiceRecord.objects.filter(
            specialist=specialist,
            scheduled_at=scheduled_at,
            status=ServiceRecord.Status.PLANNED,
        ).exists():
            raise serializers.ValidationError(
                {"scheduled_at": "This time slot is already booked."}
            )
