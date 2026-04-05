from rest_framework import serializers

from services.models import Service, SpecialistService


class AdminServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for managing services in the admin API.
    Deleting a service archives it by setting is_active=False.

    Allows administrators to create, update and archive services.
    """

    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "description",
            "base_price",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class AdminSpecialistServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for managing specialist service assignments.

    Defines which services a specialist can provide and
    how their payout is calculated.

    Payout rules:
    - FULL  → specialist receives the full service price
    - FIXED → specialist receives a fixed payout_value
    """

    specialist_name = serializers.CharField(
        source="specialist.user.full_name", read_only=True
    )
    service_title = serializers.CharField(source="service.title", read_only=True)

    payout_type_display = serializers.CharField(
        source="get_payout_type_display", read_only=True
    )

    class Meta:
        model = SpecialistService
        fields = (
            "id",
            "specialist",
            "specialist_name",
            "service",
            "service_title",
            "payout_type",
            "payout_type_display",
            "payout_value",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        service = attrs.get("service", getattr(self.instance, "service", None))
        payout_type = attrs.get(
            "payout_type", getattr(self.instance, "payout_type", None)
        )
        payout_value = attrs.get(
            "payout_value", getattr(self.instance, "payout_value", None)
        )

        if service and not service.is_active:
            raise serializers.ValidationError(
                {"service": "Cannot assign archived service."}
            )

        if payout_type == SpecialistService.Type.FULL and payout_value:
            raise serializers.ValidationError(
                {"payout_value": "Should be empty when payout type is FULL."}
            )

        if payout_type == SpecialistService.Type.FIXED and not payout_value:
            raise serializers.ValidationError(
                {"payout_value": "Required when payout type is FIXED."}
            )

        return attrs
